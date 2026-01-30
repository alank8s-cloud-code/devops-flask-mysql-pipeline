pipeline {
    agent any

    stages {
        stage("code clone") {
            steps {
                git url: "https://github.com/Heyyprakhar1/two-tier-app.git", branch: "project"
                echo "code clone successfully..!"
            }
        }

        stage("docker build") {
            steps {
                sh "docker build -t my-app ."
                echo "docker build successfully..!"
            }
        }

        stage("DockerHub Push") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhubcred',
                    usernameVariable: 'DockerHubUser',
                    passwordVariable: 'DockerHubPass'
                )]) {
                    sh '''
                      echo "$DockerHubPass" | docker login -u "$DockerHubUser" --password-stdin
                      docker tag my-app $DockerHubUser/my-app: latest
                      docker push $DockerHubUser/my-app: latest
                    '''
                }
            }
        }

        stage("docker compose") {
            steps {
                sh "docker compose up -d"
                echo "Docker container is Up & Running..!"
            }
        }
    }

    post {
        success {
            emailext(
                from: 'heyyprakhar0106@gmail.com',
                to: 'heyyprakhar0106@gmail.com',
                subject: 'build success',
                body: 'build success'
            )
        }

        failure {
            emailext(
                from: 'heyyprakhar0106@gmail.com',
                to: 'heyyprakhar0106@gmail.com',
                subject: 'build failed',
                body: 'build failed'
            )
        }
    }
}
