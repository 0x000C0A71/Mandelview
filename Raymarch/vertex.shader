#version 330 core

layout(location = 0) in vec4 position;
layout(location = 1) in vec2 uv;


varying vec2 texcoord;



void main() {
	gl_Position = vec4(position.xy, 0.0, 1.0);
	texcoord = uv;
}