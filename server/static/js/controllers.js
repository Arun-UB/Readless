'use strict';

/* Controllers */
function UserCtrl ($scope,$http) {
	
	
	$scope.getUserInfo=function(){
	 	$scope.url='/getUserInfo';
	 	$http.get($scope.url).success(function(data,status){
	 		console.log(data);
	 		$scope.uName=data.name.trim();
	 		limit(data.subscriptions)

	 	function limit (subs) {
	 		/*var i;
	 		for(i=0;i<subs.length;i++)
	 		console.log(subs[i].feed_name)*/
	 		angular.forEach(subs,function(sub){
	 			if(sub.feed_name.length >= 18)
	 			sub.feed_name=sub.feed_name.substring(0,18)+'...';

	 		})
	 	}
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
	 	$scope.url='subscribe/'+ encodeURIComponent($scope.SubscribeKwd);
	 	console.log($scope.url)
	 	$(".close").click();
	 	$http.get($scope.url).success(function(data,status){
	 		console.log(data.status);
	 		if(data.status=="Success"){
	 			
	 			UserCtrl();
	 		}
	 	}

	 		);
	 }


		

}
function MyCtrl1() {}
MyCtrl1.$inject = [];


function MyCtrl2() {
}
MyCtrl2.$inject = [];
