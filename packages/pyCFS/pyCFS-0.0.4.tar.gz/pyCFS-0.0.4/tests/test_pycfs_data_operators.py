from pyCFS.data.io import CFSReader, cfs_types, CFSWriter
from pyCFS.data.io.cfs_types import cfs_result_type
from pyCFS.data.operators import interpolators


def test_fit_coordinates(working_directory="."):
    from pyCFS.data.operators.fit_geometry import fit_coordinates

    filename_src = f"{working_directory}/tests/data/operators/fit_geometry/fit_geometry_src.cfs"
    filename_target = f"{working_directory}/tests/data/operators/fit_geometry/fit_geometry_target.cfs"
    filename_out = f"{working_directory}/tests/data_tmp/operators/fit_geometry/fit_geometry_out.cfs"

    regions_target = ["HULL_TARGET"]
    regions_fit = ["surface"]

    transform_param_init = [0.02, 0.1, 0.07, 0, 150, 0]

    while len(transform_param_init) < len(regions_fit) * 6:
        transform_param_init.extend([0, 0, 0, 0, 0, 0])

    fit_coordinates(
        filename_src,
        filename_out,
        filename_target,
        regions_target=regions_target,
        regions_fit=regions_fit,
        transform_param_init=transform_param_init,
        init_angle_degree=True,
    )


def test_interpolators_cell2node_node2cell(working_directory="."):
    file_in = f"{working_directory}/tests/data/operators/interpolators/interpolators.cfs"
    file_out = f"{working_directory}/tests/data_tmp/operators/interpolators/cell2node_node2cell.cfs"

    quantity = "quantity"
    reg_name = "Vol"
    with CFSReader(file_in) as h5r:
        mesh_data = h5r.MeshData
        result_data_read = h5r.MultiStepData

        reg_coord = h5r.get_mesh_region_coordinates(reg_name)
        reg_conn = h5r.get_mesh_region_connectivity(reg_name)

    m_interp = interpolators.interpolation_matrix_node_to_cell(reg_coord, reg_conn)
    result_data_N2C = interpolators.apply_interpolation(
        result_data_read,
        m_interp,
        quantity,
        reg_name,
        cfs_types.cfs_result_type.NODE,
        cfs_types.cfs_result_type.ELEMENT,
        quantity_out="quantity_N2C",
    )

    m_interp = interpolators.interpolation_matrix_cell_to_node(reg_coord, reg_conn).tocsr()

    result_data_C2N = interpolators.apply_interpolation(
        result_data_N2C,
        m_interp,
        "quantity_N2C",
        reg_name,
        cfs_types.cfs_result_type.ELEMENT,
        cfs_types.cfs_result_type.NODE,
        quantity_out="quantity_C2N",
    )

    result_data_write = result_data_N2C
    result_data_write.combine_with(result_data_C2N)

    with CFSWriter(file_out) as h5w:
        h5w.create_file(mesh_data, result_data_write)


def test_interpolators_nearest_neighbor_elem(working_directory="."):
    # TODO Unit test for Nearest Neighbor interpolation
    # NN Elem -> Elem example

    source_file = f"{working_directory}/tests/data/operators/interpolators/nn_elem.cfs"
    interpolated_sim = f"{working_directory}/tests/data_tmp/operators/interpolators/nn_elem_interp.cfs"

    quantity = "acouIntensity"
    region_src_target_dict = {"internal": ["internal"]}

    with CFSReader(source_file) as h5r:
        result_data_src = h5r.MultiStepData
        mesh_data_src = h5r.MeshData

    with CFSReader(source_file) as h5r:
        mesh_data = h5r.MeshData

    result_data_nn = []
    for src_region_name in region_src_target_dict:
        source_coord = mesh_data_src.get_region_centroids(src_region_name)

        target_coord = []
        for reg_name in region_src_target_dict[src_region_name]:
            target_coord.append(mesh_data.get_region_centroids(reg_name))

        for i, reg_name in enumerate(region_src_target_dict[src_region_name]):
            m_interp = interpolators.interpolation_matrix_nearest_neighbor(
                source_coord,
                target_coord[i],
                num_neighbors=1,
                interpolation_exp=1,
                max_distance=1e-6,
            )
            m_interp = interpolators.interpolation_matrix_nearest_neighbor_inverse(
                source_coord, target_coord[i], num_neighbors=1, max_distance=1e-6
            )
            result_data_nn.append(
                interpolators.apply_interpolation(
                    result_data_src,
                    m_interp,
                    quantity=quantity,
                    region=src_region_name,
                    region_out=reg_name,
                    restype=cfs_result_type.ELEMENT,
                    restype_out=cfs_result_type.ELEMENT,
                )
            )

    result_data_disp = result_data_nn[0]
    for i in range(1, len(result_data_nn)):
        result_data_disp.combine_with(result_data_nn[i])

    with CFSWriter(interpolated_sim) as h5w:
        h5w.create_file(mesh_data, result_data_disp)


def test_interpolators_nearest_neighbor_node(working_directory="."):
    # NN Example
    source_file = f"{working_directory}/tests/data/operators/interpolators/nn_source.cfs"
    target_file = f"{working_directory}/tests/data/operators/interpolators/nn_target.cfs"
    out_file = f"{working_directory}/tests/data_tmp/operators/interpolators/nn_interpolated.cfs"

    quantity = "function"
    reg_name_source = "S_source"
    reg_name_target = ["S_target"]

    with CFSReader(source_file) as h5r:
        result_data_src = h5r.MultiStepData
        source_coord = h5r.get_mesh_region_coordinates(reg_name_source)

    with CFSReader(target_file) as h5r:
        mesh_data = h5r.MeshData
        target_coord = []
        for reg_name in reg_name_target:
            target_coord.append(h5r.get_mesh_region_coordinates(reg_name))

    result_data_nn = []
    result_data_nn_inverse = []
    for i, reg_name in enumerate(reg_name_target):
        m_interp = interpolators.interpolation_matrix_nearest_neighbor(
            source_coord, target_coord[i], num_neighbors=10, interpolation_exp=2
        )
        m_interp_inverse = interpolators.interpolation_matrix_nearest_neighbor_inverse(
            source_coord, target_coord[i], num_neighbors=10, interpolation_exp=2
        )
        result_data_nn.append(
            interpolators.apply_interpolation(
                result_data_src,
                m_interp,
                quantity=quantity,
                quantity_out=f"{quantity}_interpolated",
                region=reg_name_source,
                region_out=reg_name,
                restype=cfs_result_type.NODE,
                restype_out=cfs_result_type.NODE,
            )
        )
        result_data_nn_inverse.append(
            interpolators.apply_interpolation(
                result_data_src,
                m_interp_inverse,
                quantity=quantity,
                quantity_out=f"{quantity}_interpolated_inverse",
                region=reg_name_source,
                region_out=reg_name,
                restype=cfs_result_type.NODE,
                restype_out=cfs_result_type.NODE,
            )
        )

    result_data_write = result_data_nn[0]
    for i in range(1, len(result_data_nn)):
        result_data_write.combine_with(result_data_nn[i])

    for i in range(len(result_data_nn_inverse)):
        result_data_write.combine_with(result_data_nn_inverse[i])

    with CFSWriter(out_file) as h5w:
        h5w.create_file(mesh_data=mesh_data, result_data=result_data_write)


def test_projection_interpolation(working_directory="."):
    from pyCFS.data.operators.projection_interpolation import interpolate_region

    file_src = f"{working_directory}/tests/data/operators/projection_interpolation/source.cfs"
    file_target = f"{working_directory}/tests/data/operators/projection_interpolation/target.cfs"
    region_src_target_dict = {
        "IFs_mount_outlet": ["IFs_mount_outlet"],
        "IFs_mount_inlet": ["IFs_mount_inlet"],
        "IF_pipe_outer": ["IF_pipe_outer"],
    }

    quantity_name = "mechVelocity"

    file_out = f"{working_directory}/tests/data_tmp/operators/projection_interpolation/data_interpolated.cfs"

    return_data = interpolate_region(
        file_src=file_src,
        file_target=file_target,
        region_src_target_dict=region_src_target_dict,
        quantity_name=quantity_name,
        dim_names=["x", "y", "z"],
        is_complex=True,
        projection_direction=None,
        max_projection_distance=5e-3,
        search_radius=5e-2,
    )

    with CFSReader(file_target) as h5reader:
        target_mesh = h5reader.MeshData

    # Create output and write interpolated data
    with CFSWriter(file_out) as h5writer:
        h5writer.create_file(mesh_data=target_mesh, result_data=return_data)
