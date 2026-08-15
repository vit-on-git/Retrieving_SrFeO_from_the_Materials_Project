# 1. Keep the Python 3.10 compatibility patch at the absolute top
import typing
import typing_extensions

if not hasattr(typing, "NotRequired"):
    typing.NotRequired = typing_extensions.NotRequired

# 2. Main Script
from mp_api.client import MPRester

api_key = "*************"
with MPRester(api_key) as mpr:
    print("Connected to Materials Project successfully!")
    
    # Added 'energy_above_hull' and 'is_stable' to fields
    docs = mpr.summary.search(
        chemsys="Sr-Fe-O", 
        fields=["material_id", "formula_pretty", "structure", "energy_above_hull", "is_stable"]
    )

    # Sort the returned documents by energy_above_hull (lowest first = most stable)
    docs = sorted(docs, key=lambda x: x.energy_above_hull if x.energy_above_hull is not None else float('inf'))

    structures = {}
    print("\n--- Saving Stable/Lowest Energy Polymorphs ---")
    
    for doc in docs:
        formula = doc.formula_pretty
        
        # Filter for the target compounds
        if formula in ["SrFeO3", "Sr2Fe2O5"] or ("Sr" in formula and "Fe" in formula):
            
            # Skip highly unstable structures (e.g., more than 0.1 eV/atom above hull)
            # You can set this threshold to 0.0 if you strictly want ground-state structures
            if doc.energy_above_hull > 0.1:
                continue
                
            structures[doc.material_id] = {
                "formula": formula,
                "structure": doc.structure,
                "energy_above_hull": doc.energy_above_hull,
                "is_stable": doc.is_stable
            }
            
            # Format filename to include stability status and energy
            stability_label = "stable" if doc.is_stable else f"hull_{doc.energy_above_hull:.3f}eV"
            filename = f"{doc.material_id}_{formula}_{stability_label}.cif"
            
            # Save structure files locally
            doc.structure.to(fmt="cif", filename=filename)
            print(f"Saved: {filename} (Energy above hull: {doc.energy_above_hull:.4f} eV/atom)")
