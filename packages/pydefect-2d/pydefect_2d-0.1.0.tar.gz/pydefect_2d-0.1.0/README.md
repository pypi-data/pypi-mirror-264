# pydefect_2d

First-principles calculations are increasingly used to study dominant point defects in 2D materials.
However, the number of studies on these defects is still limited compared to those in 3D materials.
A major reason for this limitation is the difficulty in finite size corrections,
which are crucial for calculating charged defects under periodic boundary conditions (PBC).
Several groups have reported methods to correct defect formation energies,
yet routinely applying these techniques in practical applications remains challenging.
This is because each defect-charge combination requires a unique correction process.
Considering typical native defects in 2D materials, such as vacancies, antisites, interstitials,
and adsorbed atoms, requires calculations of dozens of defect-charge combinations.
Therefore, automating the correction process and minimizing computational costs is vital
for advancing defect calculations in 2D materials.
To this end, we have developed a code to automate these corrections.
We have also introduced an interpolation technique to lessen computational costs and simplify the processes.

* In this code, we employ the correction method proposed by Noh et al. [] 
and Komsa [] (NK method), which extends the FNV method [] to 2D systems.

* In the current implementation, we can treat tetragonal systems only
For convention, the directions perpendicular to the surfaces are aligned with the $z$-direction.

* In the current implementation, only VASP is supported.

* This code creates the `correction.json` and `eigenvalue_shift.yaml` files, 
which can be used in the pydefect code.

## Workflow for 2D Point Defect Calculations

1. Generate `unitcell.yaml` using pydefect

1. Create dielectric profile using either gdd or sdd subcommand.
``` pydefect_2d sdd -c 0.5 -s 0.5 -w 7.15 -wz 7.15 -u unitcell.yaml -pl ../../defects/6_30A/perfect/LOCPOT --denominator 2```

1. Perform standard defect calculations with pydefect.

1. Create the defects/correction directory.

1. Generate the 1d_gauss directory and create **gauss1_d_potential_xxxx.json** using the following command:
 ```pydefect_2d 1gm -s ../../supercell_info.json -r 0.3 0.5 -dd ../dielectric_const_dist.json```

1. Calculate Gaussian charge energy under 3D periodic boundary conditions and in isolated conditions.
```pydefect_2d gmz -z 0.3{0,2,4,6,8} 0.4{0,2,4,6,8} 0.5 -s ../../supercell_info.json -cd . -dd ../dielectric_const_dist.json```

1.  Generate **gauss_energies.json** inside defects/correction/.
```pydefect_2d ge```

1. Compute the one-dimensional potential from first-principles calculations and determine the Gaussian charge center.
```pydefect_2d 1fp -d . -pl ../../perfect/LOCPOT -od ../1d_gauss```

1. Generate slab_model.json and correction.json (at this point, it converges with pydefect).
```pydefect_2d 1sm -d Va_MoS6_-2 -dd dielectric_const_dist.json -od 1d_gauss -g correction/gauss_energies.json```
