library 'deployment'

node {
    stage ('Prepare') {
        deleteDir()
        checkout scm
    }

    stage('Deploy') {
        deployApplication('search')
    }
}
