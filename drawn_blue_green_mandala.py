
from zyxxy_canvas import create_canvas_and_axes, show_drawing_and_save_if_needed
from zyxxy_shape_functions import draw_a_triangle, draw_a_rectangle, draw_a_star, draw_a_circle, draw_a_crescent, draw_an_ellipse, draw_an_egg, draw_a_segment, draw_a_sector
from zyxxy_shape_style import set_default_patch_style, set_default_line_style, set_default_outline_style, new_layer, new_layers_outline_behind
from zyxxy_utils import tan_hours, asin_hours, sin_hours, cos_hours

#######################################################
# Creating the canvas!                               ##
ax = create_canvas_and_axes(  canvas_width = 80,
                              canvas_height = 80,
                              make_symmetric = True,
                              #tick_step = 2,
                              title = "Green And Blue Mandala",
                              model = 'https://i.pinimg.com/564x/24/be/7a/24be7a90f25924c924733e51660b5cfe.jpg',
                              model_zoom = 1.3 * 1.5,
                              background_colour='white')

#######################################################
# Now let's draw the shapes!                         ##

distance_crescents = 38
distance_circles = 30
distance_triangles = 27
triangle_height = 8
crescents_qty = 40
arc_distance = 16
arc_width = 1
init_radius_arc = 6.5

set_default_outline_style(linewidth=3)

layers_1 = new_layers_outline_behind()

for i in range(crescents_qty):
  crsc = draw_a_crescent(ax=ax, centre_x=0, centre_y=distance_crescents, width=2*tan_hours(12/(2*crescents_qty))*distance_crescents, depth_1=1.2, depth_2=2, colour=('deepskyblue' if i%2 == 0 else 'royalblue'), stretch_y=3)
  crsc.rotate(turn=12/crescents_qty*i, diamond_override=[0,0])

layers_2 = new_layers_outline_behind()

for i in range(crescents_qty):
  circle = draw_a_circle(ax=ax, centre_x=0, centre_y=distance_circles, radius=1, colour='palegreen')
  circle.rotate(turn=12/crescents_qty*(i+0.5), diamond_override=[0,0])

layers_3 = new_layers_outline_behind()
set_default_patch_style(colour="yellow")

for i in range(8):
  triangles = [draw_a_triangle(ax=ax, tip_x=0, tip_y=distance_triangles, height=triangle_height, width=3.5, turn=6) for _ in range(4)]
  for t, angle in enumerate([-0.19, -0.1, 0.1, 0.19]):
    triangles[t].rotate(turn=angle, diamond_override=[0,0])

  big_triangles = [draw_a_triangle(ax=ax, tip_x=0, tip_y=distance_triangles, height=triangle_height, width=13, turn=6) for _ in range(2)]
  for t, lr in enumerate([-1, 1]):
    big_triangles[t].rotate(turn=-lr*.1, diamond_override=[0, distance_triangles-triangle_height])
    big_triangles[t].rotate(turn=lr*.5, diamond_override=[0,0])

  for trngl in triangles + big_triangles:
    trngl.rotate(turn=12/8*i, diamond_override=[0,0])

layers_4 = new_layers_outline_behind()
print(sin_hours(12/16) * arc_distance, init_radius_arc)
assert sin_hours(12/16) * arc_distance < init_radius_arc
angle_one_arc = asin_hours(sin_hours(12/16) * arc_distance / init_radius_arc)
arc_colours = ['royalblue', 'powderblue']
centre_arc_y = arc_distance * cos_hours(12/16) - init_radius_arc * cos_hours(angle_one_arc)
for i in range(8):
  sectors = [draw_a_sector(ax=ax, 
                           angle_start=-angle_one_arc, 
                           angle_end=angle_one_arc, 
                           radius=init_radius_arc + r * arc_width, 
                           radius_2=init_radius_arc + (r+1) * arc_width, 
                           centre_x=0, 
                           centre_y=centre_arc_y,
                           colour=arc_colours[r]) for r in range(2)]
  for s in sectors:
    s.rotate(turn=12/8*i, diamond_override=[0,0])

  draw_a_segment(ax=ax, start_x=0, start_y=0, turn=12/8*i, length=centre_arc_y+init_radius_arc)


show_drawing_and_save_if_needed()