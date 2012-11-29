'use strict';

/* Controllers */
function SubscribeCtrl($scope,$http,$log){
	
	
	$scope.getUserInfo=function(){
	 	$scope.url='/getUserInfo';
	 	$http.get($scope.url).success(function(data,status){
	 		//console.log(data);
	 		$scope.uName=data.name.trim();
	 		$scope.disp_feed_name={};
	 		$scope.uCount={};
	 		angular.forEach(data.subscriptions,function(sub){	

	 			sub.site_url=sub.site_url.replace(/http:\/\//g,"");
	 			this[sub.feed_id]=(sub.feed_name);
	 			if(sub.feed_name.length >= 18){
	 			
	 			sub.feed_name=sub.feed_name.substring(0,18)+'...';

	 			}
	 		},$scope.disp_feed_name);

	 		angular.forEach(data.subscriptions,function(sub){	

	 			
	 			this[sub.feed_id]=(sub.UnreadCount);
	 				
	 		},$scope.uCount);

	 		//console.log($scope.disp_feed_name);
	 		$scope.allFeeds=data;
	 		$scope.feeds=data.subscriptions;
	 		//$log.info($scope.feeds)
	 		$scope.hide=true;
	 	}
	 	);
	 }
	 $scope.getUserInfo();


	
	 $scope.add=function(){
	 	$scope.url='subscribe/'+ encodeURIComponent($scope.SubscribeKwd);
	 	console.log($scope.url)
	 	$(".close").click();
	 	$http.get($scope.url).success(function(data,status){
	 		console.log(data.status);
	 		if(data.status=="Success"){
	 			
	 			$scope.getUserInfo();
	 		}
	 		else{
	 			$scope.msg="There was an error,try again"
	 		}
	 	}

	 		);
	 }

	$scope.loadFeeds=function(feed_id,feed_name,site_url){
		
		$scope.url='getUnreadArticles/'+feed_id;
		
		$http.get($scope.url).success(function(data,status){
	 		$scope.cur_feed_id=feed_id;
	 		$scope.cur_feed_name=$scope.disp_feed_name[feed_id];
	 		$scope.cur_site_url=site_url;
	 		$scope.articles=data.articles;
	 		$scope.hide=false;
	 			//console.log($scope.cur_site_url);
	 			//console.log($scope.articles.length);


	 		
	 	}
	 	);
	}

	$scope.unsubscribe=function(feed_id){
		$log.info(feed_id);
		$(".close").click();
		$scope.url='unsubscribe/'+feed_id;
			$http.get($scope.url).success(function(data,status){
	 		$log.info(data);
	 		$scope.getUserInfo();
	 		$scope.articles={};
	 		$scope.cur_feed_id=null;
	 		$scope.cur_feed_name=null;
	 		$scope.cur_site_url=null;
	 		$scope.hide=true;
	 		


	 		
	 	}
	 	);

	}

	
	$scope.read=function(article_id,interest){
		$scope.url='markRead/'+article_id+'/'+interest;
		$http.get($scope.url).success(function(data,status){
	 		$log.info(data);
	 		
	 		var i=0;
	 		angular.forEach($scope.articles,function(art){	
	 			//$log.info($scope.uCount[$scope.cur_feed_id])
	 			if(art.article_id==article_id){	 				
	 				 $scope.articles.splice(i,1);
	 				//$log.info($scope.articles)
	 				$scope.uCount[$scope.cur_feed_id]-=1;
	 				$log.info($scope.uCount[$scope.cur_feed_id])

	 				}		
	 			i++;
	 			
	 		},i);

	 		$log.info($scope.articles)
	 			 		
	 	});

	}
		

}
