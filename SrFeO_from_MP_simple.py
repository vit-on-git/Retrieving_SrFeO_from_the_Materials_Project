# 1. Patch the typing module for Python 3.10 compatibility
import typing
import typing_extensions

if not hasattr(typing, "NotRequired"):
  typing.NotRequired = typing_extensions.NotRequired

# 2. Your original code now runs safely
from mp_api.client import MPRester

api_key = "YOUR_MP_API_KEY"
with MPRester(api_key) as mpr:
  docs = mpr.summary.search(
      chemsys="Sr-Fe-O", fields=["material_id", "formula_pretty", "structure"]
  )

  structures = {}
  for doc in docs:
    formula = doc.formula_pretty
    if formula in ["SrFeO3", "Sr2Fe2O5"] or ("Sr" in formula and "Fe" in formula):
      structures[doc.material_id] = {
          "formula": formula,
          "structure": doc.structure,
      }
      doc.structure.to(fmt="cif", filename=f"{doc.material_id}_{formula}.cif")

