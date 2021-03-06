#version 460

layout(binding = 0) uniform sampler2DArray samplerArray;

layout(location = 0) in vec4 inColor;
layout(location = 1) in vec3 inFragTextureCoords;
layout(location = 2) in vec4 playerColor;

layout(location = 0) out vec4 outFragColor;

struct GlobalVariable {
    int value;
};

struct ObjectVariable {
    int value;
};

struct PlayerInfo {
    vec4 playerColor;
};

struct ObjectData {
    mat4 modelMatrix;
    vec4 color;
    vec2 textureMultiply;
    int textureIndex;
    int objectType;
    int playerId;
    int zIdx;
};

layout(std140, binding = 1) uniform EnvironmentData {
    mat4 projectionMatrix;
    mat4 viewMatrix;
    vec2 gridDims;
    int playerId;
    int globalVariableCount;
    int objectVariableCount;
    int highlightPlayers;
}
environmentData;

layout(std430, binding = 3) readonly buffer ObjectDataBuffer {
    uint size;
    ObjectData variables[];
}
objectDataBuffer;

layout(std430, binding = 4) readonly buffer GlobalVariableBuffer {
    GlobalVariable variables[];
}
globalVariableBuffer;

layout(std430, binding = 5) readonly buffer ObjectVariableBuffer {
    ObjectVariable variables[];
}
objectVariableBuffer;

int getObjectVariable(in int objectIndex, in int variableIndex, in int numVariables) {
    return objectVariableBuffer.variables[objectIndex * numVariables + variableIndex].value;
}

void main() {

    float glowLevel = 0.0;
    for (int i = 0; i < objectDataBuffer.size; i++) {
        ObjectData object = objectDataBuffer.variables[i];

        if (object.objectType == 6) {
            mat4 mv = environmentData.viewMatrix * object.modelMatrix;
            vec4 position = mv * vec4(0, 0, 0, 1);
            float dist_to_pixel = distance(position.xy, gl_FragCoord.xy);

            // gaussian
            glowLevel += max(0, exp(-pow(dist_to_pixel, 2.0) / 2000.0)-0.01);
        }
    }

    int time = globalVariableBuffer.variables[0].value;

    float glowPulsate = cos(time/10.0);
    glowLevel = max(0, min(glowPulsate, glowLevel));

    vec4 sprite_rgba = texture(samplerArray, inFragTextureCoords);
    vec4 glow_rgba = vec4(sprite_rgba.r, 0.7, sprite_rgba.b, sprite_rgba.a);

    //float blendFactor = step(3.0f, dot(glow_rgba.rgb, glow_rgba.rgb));

    outFragColor = mix(sprite_rgba, glow_rgba, glowLevel);
}