#version 330 core

layout(location = 0) in vec4 position;
layout(location = 1) in vec2 uv;
layout(location = 2) in vec3 vColor;


varying vec3 col;
varying vec2 texcoord;


void main() {
	gl_Position = vec4(position.xy, 0.0, 1.0);
	col = vColor;
	texcoord = uv;
}