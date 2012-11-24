'use strict';

/* Controllers */

function SubscribeCtrl($scope,$http){
	console.log($scope.SubscribeKwd);
	
	  $scope.find=function () {
	  	console.log($scope.SubscribeKwd);
	  	 $scope.url= document.location.protocol + '//ajax.googleapis.com/ajax/services/feed/find?v=1.0&callback=?&q=' + encodeURIComponent($scope.SubscribeKwd);
		$http.jsonp($scope.url).success(function find(data) {
    console.log(data);
  });
	//	$scope.fUrl= parse

}
		

}
function parse (data) {
			console.log(data);
			//return data.reponseData.entries[0].url;

		}
function MyCtrl1() {}
MyCtrl1.$inject = [];


function MyCtrl2() {
}
MyCtrl2.$inject = [];
