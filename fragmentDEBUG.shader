#version 330 core

layout(location = 0) out vec4 color;

uniform vec3 u_color;

varying vec3 col;
varying vec2 texcoord;

void main() {
	/*
	if (v_ViewNormal.z > 0) {
		color = matcap();
	}
	*/

	color = vec4(col, 1.0);
	color = vec4(texcoord, 0.0, 1.0);
}