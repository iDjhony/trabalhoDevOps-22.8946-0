pipeline {
    agent any

    stages {
        stage('Git Pull & Build Containers') {
            steps {
                script {
                    // Clona o repositório e atualiza os containers
                    git branch: "main", url: "https://github.com/Tav1nnn/trabalho_devops.git"
                    sh 'docker-compose down -v'  // Para e remove containers e volumes antigos
                    sh 'docker-compose build'   // Builda as imagens
                }
            }
        }

        stage('Start Containers & Run Tests') {
            steps {
                script {
                    // Sobe os containers necessários
                    sh 'docker-compose up -d mariadb flask mysqld_exporter prometheus grafana'
                    
                    // Espera serviços estarem prontos (ajuste conforme necessário)
                    sh 'sleep 40'  // Substituir por algo como "wait-for-it" é recomendado

                    try {
                        // Executa os testes
                        sh 'docker-compose run --rm test'
                    } catch (Exception e) {
                        // Marca o build como falha e encerra
                        currentBuild.result = 'FAILURE'
                        error "Testes falharam. Pipeline interrompido."
                    }
                }
            }
        }

        stage('Keep Application Running') {
            steps {
                script {
                    // Mantém a aplicação rodando
                    sh 'docker-compose up -d mariadb flask mysqld_exporter prometheus grafana'
                }
            }
        }
    }

    post {
        always {
            // Remove containers temporários de teste, mas mantém os principais rodando
            script {
                sh 'docker-compose rm -f test'
            }
        }

        failure {
            // Desliga todos os containers em caso de falha
            script {
                sh 'docker-compose down -v'
            }
        }

        success {
            // Mensagem de sucesso
            echo "Pipeline executado com sucesso!"
        }
    }
}
