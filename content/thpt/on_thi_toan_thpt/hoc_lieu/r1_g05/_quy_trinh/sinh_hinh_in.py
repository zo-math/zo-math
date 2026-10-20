"""Print-only arrangement, reusing the canonical scene geometry and labels."""
from pathlib import Path
import importlib.util,json

def build(name,destination):
 if name!='hop_cat_gap.svg':return False
 here=Path(__file__).resolve().parent
 spec=importlib.util.spec_from_file_location('zo_g05_print_geometry',here/'sinh_hinh.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 scene=next(s for s in json.loads(module.DATA.read_text(encoding='utf-8'))['scenes'] if s['id']=='hop_cat_gap')
 fig=module.cut_fold(scene);fig.set_size_inches(12/2.54,13/2.54)
 fig.axes[0].set_position([.03,.51,.94,.45]);fig.axes[1].set_position([.03,.01,.94,.45]);fig.canvas.draw()
 for dim in fig.zo_dimensions:module.check_dimension(dim)
 assert len(fig.zo_dimensions)==6
 for label,patch in fig.zo_labels:
  box=patch.get_window_extent();frame=fig.bbox
  assert box.x0>=frame.x0 and box.x1<=frame.x1 and box.y0>=frame.y0 and box.y1<=frame.y1,'Print label outside canvas: '+label
 fig.savefig(destination,format='pdf',metadata={'Creator':'ZO Math G05 canonical geometry, stacked print layout','CreationDate':None,'ModDate':None})
 module.plt.close(fig)
 return True
