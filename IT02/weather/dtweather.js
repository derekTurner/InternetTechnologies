/**
 * ng-weather
 * @version v0.0.1 - 2013-11-26
 * @link https://github.com/asafdav/ng-weather
 * @author Asaf David <>
 * @license MIT License, http://www.opensource.org/licenses/MIT
 */
"use strict";

angular.module("asafdav.ngWeather", [])
.value("apiEndpoint", "http://api.openweathermap.org/data/2.5/weather")
.value("iconEndpoint", "http://openweathermap.org/img/w/")

.service("weatherService", ["$http", "$q", "apiEndpoint", "iconEndpoint", function(a, b, c, d){
  /* function e(a)
  {
    this.data = a, this.getTemperature = function()
    {
      return this.data && this.data.main ? this.data.main.temp : null
    }, this.getMinTemperature = function()
    {
      return this.data && this.data.main ? this.data.main.temp_min : null
    }, this.getMaxTemperature = function()
    {
      return this.data && this.data.main ? this.data.main.temp_max : null
    }, this.getIconCode = function()
    {
      return this.data && this.data.weather && this.data.weather[0] ? this.data.weather[0].icon : null
    }, this.getIcon = function()
    {
      return d + this.getIconCode() + ".png"
    }
  }*/

  this.q = function(d, f)
  {

    var g = b.defer();
    f = "undefined" != typeof f ? f : "metric";
    var url = c + "?q=" + d + "&units=" + f + "&callback=JSON_CALLBACK&APPID={"+ "b35c6606db0394da305342d28f185dc9" +"}";

    return a.jsonp(url).then(function(a)//success  syntax angular 1.3 onwards
    {
      g.resolve(new e(a))
    }),(function(a) //failure
    {
      g.reject(a)
    }), g.promise
  }
}])  //end of service weatherService





.directive("cityWeather", ["weatherService", function(cityName)
{
  return {
    console.log(cityName);
    scope:
    {
      cityWeather: "&"
    },
    restrict: "A",// this is an attribute directive E is for elements
    template: '{{}}'+'<div class="weather-widget">'+
              '<h1>Temperature in {{city}}'+//' <img ng-src="{{weather.getIcon()}}" /></h1>'+
              '<h3>Current: {{weather.getTemperature()}}&deg;C</h3>'+
              '<h4>Min: {{weather.getMinTemperature()}}&deg;C, '+
                  'Max: {{weather.getMaxTemperature()}}&deg;C '+
              '</h4></div>',

    /*link: function(b)
    {
      b.$watch("cityWeather", function()
      {
        b.city = b.$eval(b.cityWeather), cityName.q(b.city).then(function(a)
        {
          b.weather = cityName
        }, function()
        {
          b.weather = null
        })
      })
    } */
  }
}]);
