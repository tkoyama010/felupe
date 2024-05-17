from . import (
    constitution,
    dof,
    element,
    math,
    mechanics,
    mesh,
    quadrature,
    region,
    solve,
    tools,
)
from .__about__ import __version__
from .assembly import IntegralForm
from .assembly.expression import Form
from .constitution import (
    AreaChange,
    CompositeMaterial,
    ConstitutiveMaterial,
    Hyperelastic,
    LinearElastic,
    LinearElasticLargeStrain,
    LinearElasticPlaneStrain,
    LinearElasticPlaneStress,
    LinearElasticPlasticIsotropicHardening,
    LineChange,
    Material,
    MaterialAD,
    MaterialStrain,
    NearlyIncompressible,
    NeoHooke,
    NeoHookeCompressible,
    OgdenRoxburgh,
    ThreeFieldVariation,
    ViewMaterial,
    ViewMaterialIncompressible,
    VolumeChange,
    Volumetric,
    alexander,
    anssari_benam_bucchi,
    arruda_boyce,
    constitutive_material,
    extended_tube,
    finite_strain_viscoelastic,
    isochoric_volumetric_split,
    linear_elastic,
    linear_elastic_plastic_isotropic_hardening,
    lopez_pamies,
    miehe_goektepe_lulei,
    mooney_rivlin,
    morph,
    morph_representative_directions,
    neo_hooke,
    ogden,
    ogden_roxburgh,
    saint_venant_kirchhoff,
    third_order_deformation,
    total_lagrange,
    updated_lagrange,
    van_der_waals,
    yeoh,
)
from .dof import Boundary
from .element import ArbitraryOrderLagrange as ArbitraryOrderLagrangeElement
from .element import (
    BiQuadraticQuad,
    ConstantHexahedron,
    ConstantQuad,
    Hexahedron,
    Line,
    Quad,
    QuadraticHexahedron,
    QuadraticQuad,
    QuadraticTetra,
    QuadraticTriangle,
    Tetra,
    TetraMINI,
    Triangle,
    TriangleMINI,
    TriQuadraticHexahedron,
)
from .field import (
    Field,
    FieldAxisymmetric,
    FieldContainer,
    FieldDual,
    FieldPlaneStrain,
    FieldsMixed,
)
from .mechanics import (
    CharacteristicCurve,
    FormItem,
    Job,
    MultiPointConstraint,
    MultiPointContact,
    PointLoad,
    SolidBody,
    SolidBodyGravity,
    SolidBodyNearlyIncompressible,
    SolidBodyPressure,
    StateNearlyIncompressible,
    Step,
)
from .mesh import Circle, Cube, Grid, Mesh, MeshContainer, Point, Rectangle
from .quadrature import BazantOh, GaussLegendre, GaussLegendreBoundary
from .quadrature import Tetrahedron as TetrahedronQuadrature
from .quadrature import Triangle as TriangleQuadrature
from .region import (
    Region,
    RegionBiQuadraticQuad,
    RegionBiQuadraticQuadBoundary,
    RegionBoundary,
    RegionConstantHexahedron,
    RegionConstantQuad,
    RegionHexahedron,
    RegionHexahedronBoundary,
    RegionLagrange,
    RegionQuad,
    RegionQuadBoundary,
    RegionQuadraticHexahedron,
    RegionQuadraticHexahedronBoundary,
    RegionQuadraticQuad,
    RegionQuadraticQuadBoundary,
    RegionQuadraticTetra,
    RegionQuadraticTriangle,
    RegionTetra,
    RegionTetraMINI,
    RegionTriangle,
    RegionTriangleMINI,
    RegionTriQuadraticHexahedron,
    RegionTriQuadraticHexahedronBoundary,
)
from .tools import ViewField, ViewMesh
from .tools import ViewSolid
from .tools import ViewSolid as View
from .tools import ViewXdmf, newtonrhapson, project, runs_on, save, topoints

UserMaterial = Material  # alias to be removed in v8.0.0
UserMaterialStrain = MaterialStrain  # alias to be removed in v8.0.0
UserMaterialHyperelastic = Hyperelastic  # alias to be removed in v8.0.0

__all__ = [
    "__version__",
    "constitution",
    "dof",
    "element",
    "math",
    "mechanics",
    "mesh",
    "quadrature",
    "region",
    "solve",
    "tools",
    "Form",
    "FormItem",
    "IntegralForm",
    "Basis",
    "Field",
    "FieldDual",
    "FieldAxisymmetric",
    "FieldContainer",
    "FieldPlaneStrain",
    "FieldsMixed",
    "AreaChange",
    "LinearElastic",
    "LinearElasticLargeStrain",
    "LinearElasticPlaneStrain",
    "LinearElasticPlaneStress",
    "LinearElasticPlasticIsotropicHardening",
    "LineChange",
    "CompositeMaterial",
    "Volumetric",
    "NeoHooke",
    "NeoHookeCompressible",
    "OgdenRoxburgh",
    "ThreeFieldVariation",
    "NearlyIncompressible",
    "Material",
    "MaterialStrain",
    "Hyperelastic",
    "total_lagrange",
    "updated_lagrange",
    "MaterialAD",
    "ViewMaterial",
    "ViewMaterialIncompressible",
    "ConstitutiveMaterial",
    "constitutive_material",
    "VolumeChange",
    "linear_elastic",
    "linear_elastic_plastic_isotropic_hardening",
    "alexander",
    "anssari_benam_bucchi",
    "arruda_boyce",
    "extended_tube",
    "finite_strain_viscoelastic",
    "isochoric_volumetric_split",
    "lopez_pamies",
    "miehe_goektepe_lulei",
    "mooney_rivlin",
    "morph",
    "morph_representative_directions",
    "neo_hooke",
    "ogden",
    "saint_venant_kirchhoff",
    "third_order_deformation",
    "van_der_waals",
    "yeoh",
    "Boundary",
    "ArbitraryOrderLagrangeElement",
    "BiQuadraticQuad",
    "ConstantHexahedron",
    "ConstantQuad",
    "Hexahedron",
    "Line",
    "Quad",
    "QuadraticHexahedron",
    "QuadraticQuad",
    "QuadraticTetra",
    "QuadraticTriangle",
    "Tetra",
    "TetraMINI",
    "Triangle",
    "TriangleMINI",
    "TriQuadraticHexahedron",
    "Circle",
    "Cube",
    "Grid",
    "Mesh",
    "MeshContainer",
    "Point",
    "Rectangle",
    "CharacteristicCurve",
    "Job",
    "PointLoad",
    "SolidBody",
    "SolidBodyGravity",
    "SolidBodyNearlyIncompressible",
    "SolidBodyPressure",
    "StateNearlyIncompressible",
    "Step",
    "MultiPointConstraint",
    "MultiPointContact",
    "GaussLegendre",
    "GaussLegendreBoundary",
    "TetrahedronQuadrature",
    "TriangleQuadrature",
    "BazantOh",
    "Region",
    "RegionBiQuadraticQuad",
    "RegionBiQuadraticQuadBoundary",
    "RegionBoundary",
    "RegionConstantHexahedron",
    "RegionConstantQuad",
    "RegionHexahedron",
    "RegionHexahedronBoundary",
    "RegionLagrange",
    "RegionQuad",
    "RegionQuadBoundary",
    "RegionQuadraticHexahedron",
    "RegionQuadraticHexahedronBoundary",
    "RegionQuadraticQuad",
    "RegionQuadraticQuadBoundary",
    "RegionQuadraticTetra",
    "RegionQuadraticTriangle",
    "RegionTetra",
    "RegionTetraMINI",
    "RegionTriangle",
    "RegionTriangleMINI",
    "RegionTriQuadraticHexahedron",
    "RegionTriQuadraticHexahedronBoundary",
    "newtonrhapson",
    "project",
    "save",
    "topoints",
    "View",
    "ViewField",
    "ViewMesh",
    "ViewXdmf",
    "ViewSolid",
    "runs_on",
    "UserMaterial",  # to be removed in v8.0.0
    "UserMaterialStrain",  # to be removed in v8.0.0
    "UserMaterialHyperelastic",  # to be removed in v8.0.0
]
