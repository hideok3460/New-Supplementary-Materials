from pathlib import Path
import sys,json,hashlib,csv,shutil,collections
import numpy as np,pandas as pd
sys.dont_write_bytecode=True
import argparse
parser=argparse.ArgumentParser(description="Recheck preserved run02 records without IBM access or new optimization.")
parser.add_argument("--hardware-root",type=Path,required=True,help="Extracted ibm_phoenix_run02_reproducible directory")
parser.add_argument("--output-root",type=Path,default=Path("audit_recheck"),help="New audit/table output directory")
args=parser.parse_args()
ROOT=args.hardware_root.expanduser().resolve()
OUT=args.output_root.expanduser().resolve()
if not (ROOT/"PACKAGE_FILE_SHA256.txt").is_file():
 raise SystemExit("The hardware root must contain PACKAGE_FILE_SHA256.txt and the released Python files.")
if OUT==ROOT or ROOT in OUT.parents:
 raise SystemExit("Do not write audit outputs inside the immutable hardware archive.")
for folder in (OUT/"audit",OUT/"manuscript/tables",OUT/"supplement/tables"):
 folder.mkdir(parents=True,exist_ok=True)

A=ROOT/'Results/02_hardware/full_4resources_run02'
R=ROOT/json.loads((A/'latest_gof_repair.json').read_text())['repair_directory']
sys.path.insert(0,str(ROOT))
from phoenix_hardware_evidence import verify_saved_hardware
from quantum_core import tomography,frame,encoding,resource,transfer_unitary,partial_receiver,discarded,ket,apply_choi,PROBES,concurrence
from reanalyse_counts import load_groups,state_metrics
from datetime import datetime
log={}
log['input_archive']='applsci-fixed4.zip'
log['hardware']=verify_saved_hardware(ROOT,check_raw=True)
lines=(ROOT/'PACKAGE_FILE_SHA256.txt').read_text().splitlines()
verified=0
for line in lines:
 h,n=line.split('  ',1)
 assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
 verified+=1
log['manifest_entries_verified']=verified
log['count_file_sha256']=hashlib.sha256((A/'receiver_counts.json').read_bytes()).hexdigest()
error_mat=[];error_metric=[];error_process=[];err_ci=[];counts={};summ={};tables={}
for proto in ['network','direct_preparation','swap_transfer']:
 _,groups,_=load_groups(A/'receiver_counts.json',proto)
 d=R/proto
 s=pd.read_csv(d/'measured_state_phases_concurrence.csv',dtype={'coherence_row':str,'coherence_col':str})
 c=pd.read_csv(d/'measured_cptni_fits.csv');g=pd.read_csv(d/'count_level_gof.csv')
 tables[proto]=(s,c,g)
 for _,row in s.iterrows():
  source='raw' if row.recovery=='frame_tracked' else row.recovery
  kk=(row.acquisition_id,int(row.M1),int(row.M2),int(row.x),int(row.m),source,'chi')
  rr=tomography(groups[kk]);C=frame(row.x,row.m,row.M1,row.M2)
  if row.recovery=='frame_tracked':rr=C.conj().T@rr@C
  saved=np.load(d/row.matrix_file,allow_pickle=False)
  error_mat.append(float(np.max(np.abs(rr-saved))))
  vals=state_metrics(rr,int(row.x),int(row.m),int(row.M1),int(row.M2),row.recovery)
  for k in ('fidelity','concurrence','phase_rad','code_population','purity','negativity'):
   error_metric.append(float(abs(vals[k]-row[k])))
  bb=np.load(d/row.bootstrap_file,allow_pickle=False)
  for k in ('fidelity','concurrence','code_population'):
   assert bb[k].shape==(500,)
   lo,hi=np.quantile(bb[k],[.025,.975]);err_ci.extend([abs(lo-row[k+'_lo']),abs(hi-row[k+'_hi'])])
  delta=np.angle(np.exp(1j*(bb['phase_rad']-row.phase_rad)));lo,hi=row.phase_rad+np.quantile(delta,[.025,.975]);err_ci.extend([abs(lo-row.phase_rad_lo),abs(hi-row.phase_rad_hi)])
 for _,row in c.iterrows():
  source=row.source_recovery;J=np.load(d/row.matrix_file);V=encoding();C=frame(row.x,row.m,row.M1,row.M2)
  residual=0
  for probe in ['0','1','+','+i']:
   rr=tomography(groups[(row.acquisition_id,int(row.M1),int(row.M2),int(row.x),int(row.m),source,probe)])
   if source=='raw':rr=C.conj().T@rr@C
   B=V.conj().T@rr@V;pred=apply_choi(J,np.outer(PROBES[probe],PROBES[probe].conj()));residual+=np.linalg.norm(pred-B)**2
  phi=np.array([1,0,0,1])/np.sqrt(2)
  error_process.extend([abs(residual-row.block_residual),abs(np.trace(J).real/2-row.survival),abs((phi@J@phi).real/2-row.identity_overlap)])
  bb=np.load(d/row.bootstrap_file,allow_pickle=False)
  for k in ['survival','identity_overlap','block_residual']:
   assert len(bb[k])==500
   lo,hi=np.quantile(bb[k],[.025,.975]);err_ci.extend([abs(lo-row[k+'_lo']),abs(hi-row[k+'_hi'])])
 for _,row in g.iterrows():
  b=np.load(d/'gof_details'/row.process_id/'parametric_null_statistics.npz',allow_pickle=False)
  for statistic,key,pcol in [('pearson_X2','pearson_X2','pearson_parametric_p'),('block_objective','block_residual','block_parametric_p')]:
   vals=b[key];assert len(vals)==500
   pp=(1+np.count_nonzero(vals>=row[statistic]))/501;assert abs(pp-row[pcol])<1e-12
 counts[proto]={'state_rows':len(s),'process_rows':len(c),'gof_rows':len(g)}
print("AUDIT MAXIMA",max(error_mat),max(error_metric),max(error_process),max(err_ci)); assert max(error_mat)<1e-12 and max(error_metric)<1e-7 and max(error_process)<1e-10 and max(err_ci)<1e-10
log['counts']=counts
log['independent_numeric_checks']={'max_state_matrix_difference':max(error_mat),'max_reported_state_metric_difference':max(error_metric),'max_process_metric_difference':float(max(error_process)),'max_CI_difference':float(max(err_ci)),'checks_include_all_50_state_rows_all_34_channel_rows_all_34_gof_rows':True,'full_bootstrap_optimization_repeated':False,'new_qpu_jobs':0}
# Full operator-space identity check, including the loss of coherence across the parity sectors.
err64=[];err128=[];err256=[]
for M1 in [0,1]:
 for M2 in [0,1]:
  for x in [0,1]:
   for m in [0,1]:
    U=transfer_unitary(x,m);G=resource(m,M1,M2);C=frame(x,m,M1,M2)
    for y in [0,1]:
     V=encoding(y);D=discarded(x,m,M1,y)
     for j in [0,1]:
      actual=U@np.kron(G,V[:,j]);target=(-1)**(m*M1+M2*y)*np.kron(C@V[:,j],D)
      err64.append(float(np.max(np.abs(actual-target))))
     for j in [0,1]:
      for k in [0,1]:
       E=np.outer(V[:,j],V[:,k].conj());raw=partial_receiver(U@np.kron(np.outer(G,G.conj()),E)@U.conj().T)
       err128.append(float(np.max(np.abs(C.conj().T@raw@C-E))))
    P0=encoding(0)@encoding(0).conj().T;P1=encoding(1)@encoding(1).conj().T
    for j in range(4):
     for k in range(4):
      E=np.zeros((4,4),complex);E[j,k]=1
      raw=partial_receiver(U@np.kron(np.outer(G,G.conj()),E)@U.conj().T)
      err256.append(float(np.max(np.abs(C.conj().T@raw@C-P0@E@P0-P1@E@P1))))
log['theory_check']={f'{name}_count':len(arr) for name,arr in [('basis',err64),('code_operator',err128),('full_operator',err256)]}
log['theory_check']['max_absolute_errors']=[max(err64),max(err128),max(err256)]
# Tables generated directly from preserved CSVs
T=OUT/'manuscript/tables';T.mkdir(exist_ok=True);ST=OUT/'supplement/tables';ST.mkdir(exist_ok=True)
# Helpers produce row-only input files with normal academic precision.
def f(v,d=4):return f'{float(v):.{d}f}'
def ci(row,key,d=4):return f'{f(row[key],d)} [{f(row[key+"_lo"],d)}, {f(row[key+"_hi"],d)}]'
def sci(v):
 if abs(v)<1e-12:return r'$<10^{-12}$'
 a,b=f'{v:.2e}'.split('e');return '$'+a+r'\times10^{'+str(int(b))+'}$'
def save(path,rows):path.write_text('\n'.join(rows)+'\n')
s,c,g=tables['network'];phys=s[s.recovery=='physical'];raw=s[s.recovery=='raw']
rows=[]
for _,d in phys.sort_values(['M1','M2','x','m']).iterrows():
 rr=raw[(raw.M1==d.M1)&(raw.M2==d.M2)&(raw.x==d.x)&(raw.m==d.m)].iloc[0]
 rows.append(f'$({d.M1},{d.M2})$ & $({d.x},{d.m})$ & $\\mathcal{{C}}_{{{rr.evaluation_code_y}}}$ & {ci(rr,"phase_rad",3)} & {ci(d,"phase_rad",3)} '+r'\\')
save(T/'phase_rows.tex',rows)
rows=[]
for _,d in phys.sort_values(['M1','M2','x','m']).iterrows():
 rows.append(f'$({d.M1},{d.M2})$ & $({d.x},{d.m})$ & {ci(d,"fidelity")} & {ci(d,"concurrence")} & {f(d.code_population)} '+r'\\')
save(T/'state_rows.tex',rows)
rows=[]
cp=c[c.recovery=='physical'];gp=g[g.recovery=='physical'];joined=cp.merge(gp,on=['M1','M2','x','m'],suffixes=('','_gof'))
for _,d in joined.sort_values(['M1','M2','x','m']).iterrows():
 rows.append(f'$({d.M1},{d.M2})$ & $({d.x},{d.m})$ & {sci(d.block_residual)} & {sci(d.block_null_q95)} & {f(d.pearson_X2,2)} & {f(d.pearson_parametric_p,4)} & {f(d.block_parametric_p,4)} '+r'\\')
save(T/'gof_rows.tex',rows)
# Full numerical result tables, including raw and frame tracked states, all process/Gof rows.
for proto,(s0,c0,g0) in tables.items():
 pd.DataFrame(s0).to_csv(OUT/'audit'/f'{proto}_state_values.csv',index=False)
 for recovery in s0.recovery.unique():
  rows=[]
  for _,d in s0[s0.recovery==recovery].sort_values(['M1','M2','x','m']).iterrows():
   rows.append(f'$({d.M1},{d.M2};{d.x},{d.m})$ & {ci(d,"phase_rad",4)} & {ci(d,"concurrence",4)} & {ci(d,"code_population",4)} '+r'\\')
  save(ST/f'{proto}_{recovery}_state.tex',rows)
 for recovery in c0.recovery.unique():
  rows=[];grow=[]
  cj=c0[c0.recovery==recovery].merge(g0,on='process_id',suffixes=('','_gof'))
  for _,d in cj.sort_values(['M1','M2','x','m']).iterrows():
   rows.append(f'$({d.M1},{d.M2};{d.x},{d.m})$ & {ci(d,"survival")} & {ci(d,"identity_overlap")} & {sci(d.block_residual)} & {f(d.bootstrap_boundary_fraction,3)} '+r'\\')
   grow.append(f'$({d.M1},{d.M2};{d.x},{d.m})$ & {f(d.pearson_X2,3)} & {f(d.pearson_null_q95,3)} & {f(d.pearson_parametric_p)} & {sci(d.block_residual)} & {sci(d.block_null_q95)} & {f(d.block_parametric_p)} '+r'\\')
  save(ST/f'{proto}_{recovery}_process.tex',rows);save(ST/f'{proto}_{recovery}_gof.tex',grow)
# Combine physical fidelity/concurrence with baselines and cost summary
layout=pd.read_csv(R/'hardware_diagnostics/final_layouts_and_counts_mapping.csv')
over=pd.read_csv(R/'hardware_diagnostics/compiled_recovery_overhead.csv')
resp=pd.read_csv(R/'hardware_diagnostics/readout_response_summary.csv')
cost=pd.read_csv(R/'hardware_diagnostics/calibration_gate_diagnostics.csv')
cal=json.loads((A/'calibration_at_submission.json').read_text())['properties']
qubit_rows=[]
for q in [60,61,70,71,80]:
 vals={d['name']:(d['value'],d['unit']) for d in cal['qubits'][q]}
 qubit_rows.append({'physical_qubit':q,**{k:vals[k][0] for k in ['T1','T2','readout_error','readout_length']}})
pd.DataFrame(qubit_rows).to_csv(OUT/'audit/calibration_qubits.csv',index=False)
save(ST/'calibration_qubits.tex',[f'{d["physical_qubit"]} & {f(d["T1"],2)} & {f(d["T2"],2)} & {f(d["readout_error"],5)} & {f(d["readout_length"],0)} '+r'\\' for d in qubit_rows])
rows=[]
for _,d in resp.iterrows():rows.append(f'({d.physical_q3},{d.physical_q4}) & {d.design_epoch} & {f(d.mean_assignment_success,5)} & {f(d.response_condition_number,4)} '+r'\\')
save(ST/'readout_rows.tex',rows)
rows=[]
for key,d in over.groupby(['M1','M2','x','m']):
 rr=pd.read_csv(R/'network/measured_recovery_comparison.csv');dd=rr[(rr.M1==key[0])&(rr.M2==key[1])&(rr.x==key[2])&(rr.m==key[3])].iloc[0]
 rows.append(f'$({key[0]},{key[1]};{key[2]},{key[3]})$ & {int(d.depth_difference.iloc[0])} & 0 & {f(dd.physical_minus_tracked_fidelity)} [{f(dd.fidelity_difference_lo)}, {f(dd.fidelity_difference_hi)}] '+r'\\')
save(ST/'overhead_rows.tex',rows)
# Calibration/coherence and timing summary
jobs=json.loads((A/'job_metadata.json').read_text()); submitted=json.loads((A/'submitted_jobs.json').read_text());rows=[]
for d in jobs:
 t=d['metrics']['timestamps'];entry=next(j for j in submitted if j['job_id']==d['job_id'])
 rows.append(r'\texttt{'+d['job_id']+'} & '+str(entry['stop']-entry['start'])+' & '+t['running'][11:19]+' & '+t['finished'][11:19]+r' \\')
save(ST/'jobs_rows.tex',rows)
# Static summaries for writing and validation
p=phys
log['main_metrics']={k:{'min':float(p[k].min()),'max':float(p[k].max())} for k in ['fidelity','concurrence','phase_error_rad','code_population']}
log['phase_ideal_inside_95_interval_count']=int(((p.phase_rad_lo<=-np.pi/3)&(p.phase_rad_hi>=-np.pi/3)).sum())
log['all_physical_concurrence_lower_bounds_positive']=bool((p.concurrence_lo>0).all())
log['physical_bootstrap_boundary_fraction_range']=[float(cp.bootstrap_boundary_fraction.min()),float(cp.bootstrap_boundary_fraction.max())]
log['compiled_network_gates']=sorted(layout[layout.protocol=='network'].two_qubit_gates.unique().tolist())
log['compiled_network_depth']={rec:[int(gr.depth.min()),int(gr.depth.max())] for rec,gr in layout[layout.protocol=='network'].groupby('recovery')}
log['recovery_depth_overhead']={'pairs':len(over),'min':int(over.depth_difference.min()),'max':int(over.depth_difference.max()),'mean':float(over.depth_difference.mean()),'two_qubit_gate_increase_max':int(over.two_qubit_gate_difference.max())}
log['calibration_summary']={'snapshot':json.loads((A/'calibration_at_submission.json').read_text())['captured_utc'],'network_gate_duration_sum_seconds':[float(cost[cost.protocol=='network'].sum_native_gate_durations_s.min()),float(cost[cost.protocol=='network'].sum_native_gate_durations_s.max())],'network_independent_proxy':[float(cost[cost.protocol=='network'].independent_no_error_proxy.min()),float(cost[cost.protocol=='network'].independent_no_error_proxy.max())]}
cor=pd.read_csv(R/'hardware_diagnostics/receiver_discarded_correlations.csv');dis=pd.read_csv(R/'hardware_diagnostics/discarded_expectations.csv');log['witnesses']={'marginal_rows':len(dis),'correlation_rows':len(cor),'pointwise_intervals_excluding_zero':int(((cor.correlation_lo>0)|(cor.correlation_hi<0)).sum()),'max_abs_correlation':float(cor.connected_correlation.abs().max())}
log['solver_retries']={}
for proto in ['direct_preparation','swap_transfer']:
 rows=[json.loads(l) for l in next((R/proto/'gof_details').glob('*/solver_audit.jsonl')).read_text().splitlines()]
 log['solver_retries'][proto]=dict(collections.Counter(d['method'] for d in rows))
log['not_performed']=['No new IBM job or remote authentication','No repeat of full 500-refit numerical optimization','No independent coverage study','No cross-backend or repeated-day acquisition']
(OUT/'audit/data_audit.json').write_text(json.dumps(log,indent=2))

print(json.dumps(log,indent=2))
