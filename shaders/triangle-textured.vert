#version 460

layout(location = 0) in vec3 inPosition;
layout(location = 1) in vec2 inFragTextureCoords;

layout(location = 0) out vec4 outColor;
layout(location = 1) out vec3 outFragTextureCoords;
layout(location = 2) out vec4 outPlayerColor;

out gl_PerVertex {
  vec4 gl_Position;
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

struct GlobalVariable {
    int value;
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

layout(push_constant) uniform PushConsts {
  int idx;
}
pushConsts;


void main() {
  ObjectData object = objectDataBuffer.variables[pushConsts.idx];

  outFragTextureCoords = vec3(
      inFragTextureCoords.x * object.textureMultiply.x,
      inFragTextureCoords.y * object.textureMultiply.y,
      object.textureIndex);

    if (object.objectType == 1) { // cralwer
        int time = globalVariableBuffer.variables[0].value;
        float x = 0.1 * cos(time/2.0);
        object.modelMatrix[3][1] += x;
    }

    if(object.objectType == 2) { // egg
        int time = globalVariableBuffer.variables[0].value;
        float x = sin(time/20.0)*0.5;
        object.modelMatrix[0][0] += x;
        object.modelMatrix[1][1] += x;
    }

  mat4 mvp = environmentData.projectionMatrix * environmentData.viewMatrix * object.modelMatrix;



  gl_Position = mvp * vec4(
                          inPosition.x,
                          inPosition.y,
                          inPosition.z,
                          1.);
}