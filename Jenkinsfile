library 'libcommon'

node {
    stage ('Prepare') {
        deleteDir()
        checkout scm
    }

    stage('Deploy') {
        libcommon.deploy('search')
    }
}
