"""Test script for testing geometry creation library

Offers sample methods a server could implement using a sphere
"""

import asyncio

import pandas as pd
import matplotlib
import rigatoni

from context import geometry as geo

# 42 vertices for sphere
vertices = [[-0.000000, -0.500000, -0.000000], [0.361804, -0.223610, 0.262863],
            [-0.138194, -0.223610, 0.425325],  [-0.447213, -0.223608, -0.000000],
            [-0.138194, -0.223610, -0.425325], [0.361804, -0.223610, -0.262863],
            [0.138194, 0.223610, 0.425325],    [-0.361804, 0.223610, 0.262863],
            [-0.361804, 0.223610, -0.262863],  [0.138194, 0.223610, -0.425325],
            [0.447213, 0.223608, -0.000000],   [-0.000000, 0.500000, -0.000000],
            [-0.081228, -0.425327, 0.249998],  [0.212661, -0.425327, 0.154506],
            [0.131434, -0.262869, 0.404506],   [0.425324, -0.262868, -0.000000],
            [0.212661, -0.425327, -0.154506],  [-0.262865, -0.425326, -0.000000],
            [-0.344095, -0.262868, 0.249998],  [-0.081228, -0.425327, -0.249998],
            [-0.344095, -0.262868, -0.249998], [0.131434, -0.262869, -0.404506],
            [0.475529, 0.000000, 0.154506],    [0.475529, 0.000000, -0.154506],
            [-0.000000, 0.000000, 0.500000],   [0.293893, 0.000000, 0.404508],
            [-0.475529, 0.000000, 0.154506],   [-0.293893, 0.000000, 0.404508],
            [-0.293893, 0.000000, -0.404508],  [-0.475529, 0.000000, -0.154506],
            [0.293893, 0.000000, -0.404508],   [-0.000000, 0.000000, -0.500000],
            [0.344095, 0.262868, 0.249998],    [-0.131434, 0.262869, 0.404506],
            [-0.425324, 0.262868, -0.000000],  [-0.131434, 0.262869, -0.404506],
            [0.344095, 0.262868, -0.249998],   [0.081228, 0.425327, 0.249998],
            [0.262865, 0.425326, -0.000000],   [-0.212661, 0.425327, 0.154506],
            [-0.212661, 0.425327, -0.154506],  [0.081228, 0.425327, -0.249998]]

# 80 triangles
indices =  [[0, 13, 12],  [1, 13, 15],  [0, 12, 17],  [0, 17, 19],
            [0, 19, 16],  [1, 15, 22],  [2, 14, 24],  [3, 18, 26],
            [4, 20, 28],  [5, 21, 30],  [1, 22, 25],  [2, 24, 27],
            [3, 26, 29],  [4, 28, 31],  [5, 30, 23],  [6, 32, 37],
            [7, 33, 39],  [8, 34, 40],  [9, 35, 41],  [10, 36, 38],
            [38, 41, 11], [38, 36, 41], [36, 9, 41],  [41, 40, 11],
            [41, 35, 40], [35, 8, 40],  [40, 39, 11], [40, 34, 39],
            [34, 7, 39],  [39, 37, 11], [39, 33, 37], [33, 6, 37],
            [37, 38, 11], [37, 32, 38], [32, 10, 38], [23, 36, 10],
            [23, 30, 36], [30, 9, 36],  [31, 35, 9],  [31, 28, 35],
            [28, 8, 35],  [29, 34, 8],  [29, 26, 34], [26, 7, 34],
            [27, 33, 7],  [27, 24, 33], [24, 6, 33],  [25, 32, 6],
            [25, 22, 32], [22, 10, 32], [30, 31, 9],  [30, 21, 31],
            [21, 4, 31],  [28, 29, 8],  [28, 20, 29], [20, 3, 29],
            [26, 27, 7],  [26, 18, 27], [18, 2, 27],  [24, 25, 6],
            [24, 14, 25], [14, 1, 25],  [22, 23, 10], [22, 15, 23],
            [15, 5, 23],  [16, 21, 5],  [16, 19, 21], [19, 4, 21],
            [19, 20, 4],  [19, 17, 20], [17, 3, 20],  [17, 18, 3],
            [17, 12, 18], [12, 2, 18],  [15, 16, 5],  [15, 13, 16],
            [13, 0, 16],  [12, 14, 2],  [12, 13, 14], [13, 1, 14]]

colors = [[0, 255, 0, 255]] * 42


def create_spheres(server: rigatoni.Server, context, *args):
    """Test method to create two spheres"""
    
    name = "Test Sphere"
    uri_server = geo.ByteServer(port=40000)
    material = server.create_component(rigatoni.Material, name="Test Material")

    # Create Patch
    patches = []
    patch_info = geo.GeometryPatchInput(
        vertices = vertices, 
        indices = indices, 
        index_type = "TRIANGLES",
        material = material.id,
        colors = colors
    )
    patches.append(geo.build_geometry_patch(server, name, patch_info, uri_server))

    # Create geometry using patches
    sphere = server.create_component(rigatoni.Geometry, name=name, patches=patches)

    # Set instances and create an entity
    instances = geo.create_instances(
        positions=[(1,1,1,1),(2,2,2,2)],
        colors=[(1,.5,.5,1)],
    )
    entity = geo.build_entity(server, geometry=sphere, instances=instances)
    geo.export_mesh(server, sphere, "test_sphere.obj", uri_server)
    return 1


def create_new_instance(server: rigatoni.Server, context, entity_slot, entity_gen, position=None, color=None, rotation=None, scale=None):
    """Method to test instance updating"""
    
    entity = server.components[rigatoni.EntityID(entity_slot, entity_gen)]
    new_instance = geo.create_instances(position, color, rotation, scale)
    geo.add_instances(server, entity, new_instance)


def normalize_df(df: pd.DataFrame):
    """Helper to normalize values in a dataframe"""

    normalized_df = df.copy()
    for column in normalized_df:
            normalized_df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())    

    return normalized_df


def make_point_plot(server: rigatoni.Server, context, *args):
    """Test Method to generate plot-like render from data.csv"""

    name = "Test Plot"
    material = server.create_component(rigatoni.Material, name="Test Material")

    # Create patch / geometry for point geometry
    patches = []
    patch_info = geo.GeometryPatchInput(
        vertices = vertices, 
        indices = indices, 
        index_type = "TRIANGLES",
        material = material.id,
        colors = colors)
    patches.append(geo.build_geometry_patch(server, name, patch_info))
    sphere = server.create_component(rigatoni.Geometry, name=name, patches=patches)

    # Read data from data.csv and normalize
    df = pd.read_csv("/Users/aracape/development/rigatoni/tests/data.csv")
    df_scaled = normalize_df(df)
    
    # Positions
    x = list(df_scaled['Total_CNG'].apply(lambda x: x*5-2.5))
    y = list(df_scaled['Total_Elec'].apply(lambda x: x*5))
    z = list(df_scaled['Elec_price_incentive'].apply(lambda x: x*5-2.5))

    # Colors
    cmap = matplotlib.cm.get_cmap("plasma")
    cols = df_scaled['CNG_price_incentive']
    cols = [cmap(i) for i in cols]

    # Scales
    s = .1
    scls = [(i*s, i*s, i*s, i*s) for i in list(df_scaled['FCI_incentive_amount[CNG]'])]

    # Create instances of sphere to represent csv data in an entity
    instances = geo.create_instances(
        positions=[*zip(x, y, z)],
        colors=cols,
        scales=scls
    )
    entity = geo.build_entity(server, geometry=sphere, instances=instances)
    new_instance = geo.create_instances([[1,1,1]])
    geo.add_instances(server, entity, new_instance)
    return 1


def create_from_mesh(server: rigatoni.Server, context, *args):
    """Test Method to generate render from mesh"""

    name = "Test Plot"
    material = server.create_component(rigatoni.Material, name="Test Material")

    # use libraries from mesh option    
    uri_server = geo.ByteServer(port=40000)
    mesh = geo.geometry_from_mesh(server, "/Users/aracape/development/geometry_tools/tests/stanford-bunny.obj", material, name, uri_server)
    #mesh = geo.geometry_from_mesh(server, "/Users/aracape/development/test_sphere.vtk", material)
    #mesh = geo.geometry_from_mesh(server, "/Users/aracape/development/geometry_tools/tests/magvort.x3d", material)


    # Create instances of sphere to represent csv data in an entity
    instances = geo.create_instances()
    entity = geo.build_entity(server, geometry=mesh, instances=instances)

    # Test export
    geo.export_mesh(server, mesh, "test_mesh.obj", uri_server)
    return 1



# define arg documentation for injected method
instance_args = [
    rigatoni.MethodArg(name="entity_slot", doc="What're you creating an instance of?", editor_hint="ID"),
    rigatoni.MethodArg(name="entity_gen", doc="What're you creating an instance of?", editor_hint="ID"),
    rigatoni.MethodArg(name="position", doc="Where are you putting this instance", editor_hint="Vector"),
    rigatoni.MethodArg(name="color", doc="What color is this instance?", editor_hint="RGBA Vector"),
    rigatoni.MethodArg(name="rotation", doc="How is this instance rotated?", editor_hint="Vector"),
    rigatoni.MethodArg(name="scale", doc="How is this instance scaled?", editor_hint="Vector")
]

# Define starting state
starting_state = [
    rigatoni.StartingComponent(rigatoni.Method, {"name": "new_point_plot", "arg_doc": []}, make_point_plot),
    rigatoni.StartingComponent(rigatoni.Method, {"name": "create_new_instance", "arg_doc": [*instance_args]}, create_new_instance),
    rigatoni.StartingComponent(rigatoni.Method, {"name": "create_sphere", "arg_doc": []}, create_spheres),
    rigatoni.StartingComponent(rigatoni.Method, {"name": "create_from_mesh", "arg_doc": []}, create_from_mesh)
]

def main():
    asyncio.run(rigatoni.start_server(50000, starting_state))

if __name__ == "__main__":
    main()
