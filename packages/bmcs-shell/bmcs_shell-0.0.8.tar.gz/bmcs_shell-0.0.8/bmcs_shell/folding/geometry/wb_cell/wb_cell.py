import bmcs_utils.api as bu
import numpy as np
import traits.api as tr
import k3d

class WBCell(bu.Model):
    name = 'Waterbomb cell'

    plot_backend = 'k3d'

    K3D_NODES_LABELS = 'nodes_labels'
    K3D_WIREFRAME = 'wireframe'
    K3D_CELL_MESH = 'cell_mesh'

    wireframe_width = bu.Float(5)

    show_base_cell_ui = bu.Bool(True)
    show_node_labels = bu.Bool(False, GEO=True)
    show_wireframe = bu.Bool(True, GEO=True)
    opacity = bu.Float(1, GEO=True)

    callback_fun = None

    # TODO: Quick fix to make cell changes reflect in tessellations!
    @tr.observe('+GEO', post_init=False)
    def update_after_wb_cell_GEO_changes(self, event):
        if self.callback_fun is not None:
            self.callback_fun()

    ipw_view = bu.View(
        bu.Item('show_node_labels'),
        bu.Item('show_wireframe'),
        bu.Item('wireframe_width'),
    ) if show_base_cell_ui else bu.View()

    X_Ia = tr.Property(depends_on='+GEO')
    '''Array with nodal coordinates I - node, a - dimension
    '''
    @tr.cached_property
    def _get_X_Ia(self):
        return np.array([[0., 0., 0.],
                         [1000., 930.99634691, 365.02849483],
                         [-1000., 930.99634691, 365.02849483],
                         [1000., -930.99634691, 365.02849483],
                         [-1000., -930.99634691, 365.02849483],
                         [764.84218728, 0., 644.21768724],
                         [-764.84218728, 0., 644.21768724]])

    I_Fi = tr.Property(depends_on='+GEO')
    '''Triangle mapping '''
    @tr.cached_property
    def _get_I_Fi(self):
        return np.array([[0, 1, 2], [0, 3, 4], [0, 1, 5], [0, 5, 3], [0, 2, 6], [0, 6, 4]]).astype(np.int32)

    I_Li = tr.Property(depends_on='+GEO')
    @tr.cached_property
    def _get_I_Li(self):
        I_Fi = self.I_Fi
        I_Li = np.vstack(((I_Fi[:, (0, 1)]), (I_Fi[:, (0, 2)]), (I_Fi[:, (1, 2)])))
        I_Li = np.sort(I_Li, axis=1)
        return np.unique(I_Li, axis=0)

    ''' Valley crease lines'''
    I_V_Li = tr.Property(depends_on='+GEO')
    @tr.cached_property
    def _get_I_V_Li(self):
        return self.I_Li[:4]

    ''' Mountain crease lines'''
    I_M_Li = tr.Property(depends_on='+GEO')
    @tr.cached_property
    def _get_I_M_Li(self):
        return self.I_Li[4:]

    def setup_plot(self, pb):
        self.pb = pb
        k3d.plot().fetch_screenshot()
        X_Ia = self.X_Ia.astype(np.float32)
        I_Fi = self.I_Fi.astype(np.uint32)
        cell_mesh = k3d.mesh(X_Ia, I_Fi,
                                opacity=self.opacity,
                                color=0x999999,
                                side='double')
        pb.plot_fig += cell_mesh
        pb.objects[self.K3D_CELL_MESH] = cell_mesh

        if self.show_wireframe:
            self._add_wireframe_to_fig(pb, X_Ia, I_Fi)
        if self.show_node_labels:
            self._add_nodes_labels_to_fig(pb, self.X_Ia)

    def update_plot(self, pb):
        # If cell interface was embedded in higher class, this method will be called when user changes parameters
        #  However, cell mesh object will not be there because setup_plot was not called
        if self.K3D_CELL_MESH in pb.objects:
            X_Ia = self.X_Ia.astype(np.float32)
            I_Fi = self.I_Fi.astype(np.uint32)
            cell_mesh = pb.objects[self.K3D_CELL_MESH]
            cell_mesh.vertices = X_Ia
            cell_mesh.indices = I_Fi
            cell_mesh.attributes = X_Ia[:, 2]

            if self.show_wireframe:
                if self.K3D_WIREFRAME in pb.objects:
                    wireframe = pb.objects[self.K3D_WIREFRAME]
                    wireframe.width = self.wireframe_width
                    wireframe.vertices = X_Ia
                    wireframe.indices = I_Fi
                else:
                    self._add_wireframe_to_fig(pb, X_Ia, I_Fi)
            else:
                if self.K3D_WIREFRAME in pb.objects:
                        pb.clear_object(self.K3D_WIREFRAME)

            if self.show_node_labels:
                if self.K3D_NODES_LABELS in pb.objects:
                    pb.clear_object(self.K3D_NODES_LABELS)
                self._add_nodes_labels_to_fig(pb, self.X_Ia)
            else:
                if self.K3D_NODES_LABELS in pb.objects:
                    pb.clear_object(self.K3D_NODES_LABELS)

    def _add_wireframe_to_fig(self, pb, X_Ia, I_Fi):
        k3d_mesh_wireframe = k3d.lines(X_Ia,
                                      I_Fi,
                                      shader='mesh',
                                      width=self.wireframe_width,
                                      color=0x000000)
        pb.plot_fig += k3d_mesh_wireframe
        pb.objects[self.K3D_WIREFRAME] = k3d_mesh_wireframe

    def _add_nodes_labels_to_fig(self, pb, X_Ia):
        node_indicies_I = np.arange(X_Ia.shape[0])
        node_indicies_str_list = [str(idx) for idx in node_indicies_I]
        k3d_text = k3d.text(node_indicies_str_list, position=X_Ia.flatten(), label_box=False, size=0.8, color=0x00FF00)
        pb.plot_fig += k3d_text
        pb.objects[self.K3D_NODES_LABELS] = k3d_text
