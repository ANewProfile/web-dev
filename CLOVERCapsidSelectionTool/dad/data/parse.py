import itertools
import pandas as pd

df = pd.read_csv("raw.csv")
for c in df:
  df[c] = df[c].str.strip()
data = df.to_dict('records')

# headers:
# Tissue
# Cell Type
# Species
# Strain
# Purpose
# Recommended Capsid

def groupby(mlist, key):
  kf = lambda d: d[key]
  mlist = sorted(mlist, key=kf)
  grouped = {k:list(v) for k,v in itertools.groupby(mlist, key=kf)}
  return grouped

print("var capsid_selections = [");

for tissue, tissue_groups in groupby(data, "Tissue").items():
  print(f"  [\"{tissue}\", [")

  for cell_type, cell_type_groups in groupby(tissue_groups, "Cell Type").items():
    print(f"    [\"{cell_type}\", [")

    for species, species_groups in groupby(cell_type_groups, "Species").items():
      print(f"      [\"{species}\", [")

      for strain, strain_groups in groupby(species_groups, "Strain").items():
        print(f"        [\"{strain}\", [")

        for purpose, purpose_groups in groupby(strain_groups, "Purpose").items():
          print(f"          [\"{purpose}\", [")

          for data in purpose_groups:
            print("            \"%s\"," % data['Recommended Capsid'])

          print(f"           ]],") # end of purpose

        print(f"          ]],") # end of strain

      print(f"         ]],") # end of species

    print(f"        ]],") # end of cell type

  print(f"       ]],") # end of tissue

print("];")
