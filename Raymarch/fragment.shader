#version 330 core


#define MAXITERATIONS 100

layout(location = 0) out vec4 color;

uniform vec3 u_pos;
uniform vec2 u_rot;

varying vec2 texcoord;


struct mbResult {
	float bailoutIts;
	bool isInside;
};


vec2 complexSquare( vec2 complex ) {
	// (a + b)^2 = (a^2 + 2ab + b^2)
	//              real  imag  real
	// result: (a^2-b^2,  2ab)
	float real = complex.x*complex.x - complex.y*complex.y;
	float imaginary = 2*complex.x*complex.y;
	return vec2(real, imaginary); 
}



struct mbResult Mandelbrot( vec4 coord ) {
	struct mbResult result;
	result.bailoutIts = 0.0;
	result.isInside = false;

	// Spliting the 4 dimensional coordinate
	vec2 c = coord.xy;
	vec2 z = coord.zw;

	// Iterating (doing the function)
	for (int i = 0; i < MAXITERATIONS; i++) {
		z = complexSquare(z) + c;
		if (length(z) > 10000.0) {
			result.bailoutIts = float(i)/float(MAXITERATIONS-1);
			break;
		}
	}
	if (length(z) < 10000.0) {
		result.isInside = true;
	}

	return result;
}


vec3 getHue( float hue ) {
	vec3 red     = vec3(1.0, 0.0, 0.0);
	vec3 yellow  = vec3(1.0, 1.0, 0.0);
	vec3 green   = vec3(0.0, 1.0, 0.0);
	vec3 cyan    = vec3(0.0, 1.0, 1.0);
	vec3 blue    = vec3(0.0, 0.0, 1.0);

	int transition = int(hue*4.0);
	float t = mod(hue*4.0, 1.0);

	vec3 fromColor = vec3(0.0);
	vec3 toColor   = vec3(0.0);

	switch (transition) {
		case 0:
			fromColor = red;
			toColor = yellow;
			break;

		case 1:
			fromColor = yellow;
			toColor = green;
			break;

		case 2:
			fromColor = green;
			toColor = cyan;
			break;

		case 3:
			fromColor = cyan;
			toColor = blue;
			break;

		default:
			break;
	}
	return t*toColor + (1.0-t)*fromColor;
}


float DE_MB(vec3 pos) {
	struct mbResult res = Mandelbrot(vec4(pos.xzy, 0.0));
	if (res.isInside) {
		return -1.0;
	} 
	return 1./float(res.bailoutIts)/50.0;
}


float DE_Sphere(float sphereRadius, vec3 spherePosition, vec3 point) {
	return length(spherePosition - point) - sphereRadius;
}


float DE(vec3 point) {
	//point = mod(point+vec3(5.), vec3(10.))-vec3(5.);
	//float sp = DE_Sphere(1.0, vec3(0.0, 0.0, 1.0), point);
	
	//float floor = point.z;
	//return min(sp, floor);
	//return sp;


	return DE_MB(point);
}


struct marchResult {
	vec3 pos;
	bool didHit;
	int its;
};

struct marchResult march(vec3 point, vec3 dir) {
	struct marchResult result;
	for (int i = 0; i < MAXITERATIONS; i++) {
		float dist = DE(point);
		if (dist < 0.001) {
			result.pos = point;
			result.didHit = true;
			result.its = i;
			return result;
		}
		point = point + (dir * dist);
	}
	result.pos = point;
	result.didHit = false;
	result.its = 0;
	return result;
}


vec3 getNormal(vec3 pos, float deviation) {
	vec3 offset = vec3(deviation, 0.0, 0.0);
	float center = DE(pos);
	float x = DE(pos+offset.xyy);
	float y = DE(pos+offset.yxy);
	float z = DE(pos+offset.yyx);

	float dx = x-center;
	float dy = y-center;
	float dz = z-center;

	return normalize(vec3(dx, dy, dz));
}



void main() {
	//color = vec4(quadCoord, 0.0, 1.0);
	vec2 ntexcoord = texcoord-vec2(0.5);
	vec3 dir = normalize(vec3(ntexcoord.x, 1.0, ntexcoord.y));

	dir = vec3(dir.x, dir.y*cos(u_rot.x) - dir.z*sin(u_rot.x), dir.y*sin(u_rot.x) + dir.z*cos(u_rot.x));
	dir = vec3(dir.x*cos(u_rot.y) - dir.y*sin(u_rot.y), dir.x*sin(u_rot.y) + dir.y*cos(u_rot.y), dir.z);

	struct marchResult res = march(u_pos, dir);

	vec3 sunDir = normalize(vec3(0.2, -0.5, 1.0));

	float shade = 1.0;
	float ao = 1.0;

	vec3 normal = getNormal(res.pos, 0.1);

	if (res.didHit) {
		ao = pow(1.0/float(res.its), 0.4);
		/*
		struct marchResult sun = march(res.pos + normal*0.002, sunDir);
		if (sun.didHit) {
			shade = 0.5;
		}*/
	}

	float light = clamp(dot(normal, sunDir), 0.0, 1.0)/2.0 + 0.5;


	//float col = min(shade, light);

	color = vec4(vec3(ao), 1.0);
	
}