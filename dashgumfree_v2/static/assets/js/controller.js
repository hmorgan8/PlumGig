var ISSChatApp = angular.module('ISSChatApp', []);

ISSChatApp.controller('ChatController', function($scope){
    var socket=io.connect('https://'+document.domain+':'+location.port+'/iss');

    $scope.currentUser='';

    $scope.verify = function verify(){
        socket.emit('verifyuser', $scope.username, $scope.password);
    }
    
    
    // socket.on('loadhomepage', function(){
    //     console.log('loading homepage');
    //     socket.emit('updatevidlist');
    // });
    
    // socket.on('loadvids', function(vs){
    //     console.log('loading latest vids');
    //     for(i=0; i<vs.length; i++){
    //         tmp={'creator':vs[i][1],'published':vs[i][2],'URL':vs[i][4],'title':vs[i][5],'technique':vs[i][6],'genre':vs[i][7]};
    //         $scope.vidslist[i]=tmp;
    //     }
    //     $scope.$apply();
    // });
})