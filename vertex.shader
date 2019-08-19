#version 330 core

layout(location = 0) in vec4 position;
layout(location = 1) in vec2 uv;


varying vec2 quadCoord;

uniform vec2 u_quadPos;
uniform vec2 u_quadScale;


void main() {
	gl_Position = vec4(position.xy*u_quadScale+u_quadPos, 0.0, 1.0);
	quadCoord = uv;
}