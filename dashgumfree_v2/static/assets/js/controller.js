var PlumGig = angular.module('plumgigsocketio', []);

PlumGig.config(function($sceDelegateProvider){
    $sceDelegateProvider.resourceUrlWhitelist([
        'self',
        'https://www.youtube.com/**',
        'https://player.vimeo.com/video/**'
    ]);
});

PlumGig.controller('controller', function($scope){
    var socket=io.connect('https://'+document.domain+':'+location.port+'/iss');

    $scope.currentUser='';
    $scope.vidlist=[];
    $scope.medialist=[];
    $scope.genrelist=[];

    $scope.getIframeSrc = function(src){
        return src;
    };

    socket.on('connect', function(){
        console.log('connected');
        $scope.medialist=[];
        socket.emit('updatemedia');
        $scope.genrelist=[];
        socket.emit('updategenre');
    });

    $scope.verify = function verify(){
        socket.emit('verifyuser', $scope.username, $scope.password);
    };
    
    $scope.browseanimedium = function browseanimedium(vidsearch){
        console.log('getting videos by medium', vidsearch);
        $scope.vidlist=[];
        socket.emit('animationbrowse', vidsearch);
    };
    
    $scope.browsegenres = function browsegenres(vidsearch){
        console.log('getting videos by genre', vidsearch);
        $scope.vidlist=[];
        socket.emit('genrebrowse', vidsearch)
    };
    
    socket.on('updatemediumlist', function(medium){
        console.log(medium);
        $scope.medialist.push(medium);
        $scope.$apply();
    });
    
    socket.on('updategenrelist', function(genre){
        console.log(genre);
        $scope.genrelist.push(genre);
        $scope.$apply();
    });
    
    socket.on('updatevidlist', function(vid){
        console.log(vid);
        console.log(vid['URL']);
        $scope.vidlist.push(vid);
        $scope.$apply();
        console.log($scope.vidlist);
    });

})