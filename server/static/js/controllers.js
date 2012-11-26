'use strict';

/* Controllers */
function UserCtrl ($scope,$http) {
	
	
	$scope.getUserInfo=function(){
	 	$scope.url='http://localhost:5000/getUserInfo';
	 	$http.get($scope.url).success(function(data,status){
	 		console.log(data);
	 		$scope.uName=data.name.trim();
	 		$scope.feeds=data.subscriptions;
	 		//console.log($scope.feeds)
	 	}
	 	);
	 }
	 $scope.getUserInfo();
}
function SubscribeCtrl($scope,$http){
	//console.log($scope.SubscribeKwd);
	
	 /* $scope.find=function () {
	  	console.log($scope.SubscribeKwd);
	  	 $scope.url= document.location.protocol + '//ajax.googleapis.com/ajax/services/feed/find?v=1.0&callback=?&q=' + encodeURIComponent($scope.SubscribeKwd);
		$http.jsonp($scope.url).success(function find(data) {
    console.log(data);
  });
	//	$scope.fUrl= parse

}*/
	/*function handleSubAdded(data,status){
		console.log(data)
	}*/

	 $scope.add=function(){
	 	$scope.url='http://localhost:5000/subscribe/'+ encodeURIComponent($scope.SubscribeKwd);
	 	console.log($scope.url)
	 	$http.get($scope.url).success(function(data,status){
	 		console.log(data);
	 		$('#myModal').modal('hide')
	 	}

	 		);
	 }


		

}
function MyCtrl1() {}
MyCtrl1.$inject = [];


function MyCtrl2() {
}
MyCtrl2.$inject = [];
