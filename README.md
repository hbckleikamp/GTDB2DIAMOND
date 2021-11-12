# GTDB2DIAMOND
Set of simple auxiliary python scripts to help create GTDB databases for annotation with DIAMOND

<br>
This collection of scripts is d 

**Part 3: Functional analysis**

Quantification targets
|Parameter        |Default value                             | Description                                 |
|-----------------|:----------------------------------------:|---------------------------------------------|
|Pathways         |09100 Metabolism                          |list, which Kegg pathways to annotate        |
|                 |09120 Genetic Information Processing      |                                             |
|                 |09130 Environmental Information Processing|                                             |
|                 |09140 Cellular Processes                  |                                             |
|cats             |cat1,cat2,cat3,cat4                       |list, on which levels of pathways to quantify|  

<br>

Quantification parameters
|Parameter            |Default value                                             | Description                                                            |
|---------------------|:---------------------------------------------------------|------------------------------------------------------------------------|
|fun_count_targets    |["Spectral_counts","Area","Intensity"]                    |list or string, on which value should the quantification be done        |
|fun_count_methods    |["average","total","topx"]                                |list or string, how the quantification should be done                   |
|fun_topx             |5                                                         |integer, the amount of top hits selected, in case of topx quantification|                  
|normalize            |False                                                     |boolean, normalize quantification to total for that rank                |

<br>

#### How are quantities calculated?

As a default, taxa and kegg pathways are quantified with 3 different methods and 3 different targets.
The targets determine to count by either `Spectral_counts` of peptides, by `Area` or by `Intensity`, if they are available.
The user can also supply custom columns as target to count by, provided the parameters `tax_count_targets` or `fun_count_targets` are changed.

If the target is Spectral counting, the only way of quantification is a sum of total spectra. However, when quantification is done on Area, Intensity or a custom target, different quantification methods are available, such as `average`: which averages all amounts belonging to a pathway or taxa, `total`: which sums all amounts, and `topx`: which sums the topx largest amounts, where topx is supplied by a variable.

As an example: if only spectral counts are desired as outputs, the parameter configuration could be changed to:
`tax_count_targets="Spectral_counts"`, `tax_count_methods=""`, `fun_count_targets="Spectral_counts"`, `fun_count_methods=""`

<br>




#### Licensing

The pipeline is licensed with standard MIT-license. <br>
If you would like to use this pipeline in your research, please cite the following papers: 
      
-Buchfink B, Reuter K, Drost HG, "Sensitive protein alignments at tree-of-life scale using DIAMOND", Nature Methods 18, 366–368 (2021). doi:10.1038/s41592-021-01101-x
-Parks, D.H., et al. 2020. A complete domain-to-species taxonomy for Bacteria and Archaea. Nature Biotechnology, https://doi.org/10.1038/s41587-020-0501-8.


#### Contact:
-Hugo Kleimamp (Developer): H.B.C.Kleikamp@tudelft.nl<br> 
-Martin Pabst: M.Pabst@tudelft.nl<br>


#### Recommended links to other repositories:
https://github.com/bbuchfink/diamond
