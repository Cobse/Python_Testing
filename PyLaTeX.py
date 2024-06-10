import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randint(0,100,size=(10, 4)), columns=list('ABCD'))
print(df)

df.to_latex(r'C:\Users\FKJN\OneDrive - COWI\Desktop\latex_presentation\JH_Beregningsrapport\Kapittel_3\Automate.tex')