#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;
//in vec3 ObjectColor;


uniform vec3 objectColor;
//uniform vec3 lightPos;
uniform vec3 lightDir;
uniform vec3 lightColor;
uniform vec3 viewPos;

void main() {
    //*
    // Ambient lighting
    vec3 ambient = 0.2 * lightColor;

    // Diffuse lighting
    vec3 norm = normalize(Normal);
    vec3 lightDirNorm = normalize(-lightDir);
    float diff = max(dot(norm, lightDirNorm), 0.0);
    vec3 diffuse = diff * lightColor;

    // Specular lighting
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDirNorm, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColor;

    vec3 result = (ambient + diffuse) * objectColor;
    //*/
    FragColor = vec4(result, 1.0);
}
