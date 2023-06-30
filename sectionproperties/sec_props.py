import sectionproperties.pre.library.primitive_sections as sections
import sectionproperties.pre.library.steel_sections as steel_sections
from sectionproperties.pre.geometry import CompoundGeometry
from sectionproperties.pre.pre import Material
from sectionproperties.analysis.section import Section

steel = Material(
    name="Steel",
    elastic_modulus=200e3,
    poissons_ratio=0.3,
    yield_strength=500,
    density=7.85e-6,
    color="grey",
)
concrete = Material(
    name="Concrete",
    elastic_modulus=36.1e3,
    poissons_ratio=0.2,
    yield_strength=45,
    density=2.5e-6,
    color="burlywood",
)

print(steel.elastic_modulus / concrete.elastic_modulus)

rect = sections.rectangular_section(1000,500, concrete)
rebar1 = sections.circular_section(16, 10, steel)
rebar2 = sections.circular_section(16, 10, steel)
rebar3 = sections.circular_section(16, 10, steel)
rebar4 = sections.circular_section(16, 10, steel)
rebar5 = sections.circular_section(16, 10, steel)
rebar1 = rebar1.shift_section(83, 83)
rebar2 = rebar2.shift_section(283, 83)
rebar3 = rebar3.shift_section(483, 83)
rebar4 = rebar4.shift_section(683, 83)
rebar5 = rebar5.shift_section(883, 83)

combined_sect = rect + rebar1 + rebar2 + rebar3 +rebar4 + rebar5
combined_sect.plot_geometry()

mesh_size = 20
combined_sect.create_mesh(mesh_sizes=[mesh_size, mesh_size, mesh_size, mesh_size, mesh_size, mesh_size])

section = Section(combined_sect, time_info=True)
section.display_mesh_info()  # display the mesh information
#section.plot_mesh()  # plot the generated mesh

section.calculate_geometric_properties()
section.display_results()