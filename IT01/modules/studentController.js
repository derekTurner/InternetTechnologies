mainApp.controller('studentController', function($scope) {
  $scope.student = {
    firstName: "Jane",
    lastName: "Doe",
    fees:500,

    subjects:[
      {name:'Physics',marks:70},
      {name:'Chemistry',marks:80},
      {name:'Math',marks:65},
      {name:'English',marks:75},
      {name:'Music',marks:67}
    ],

    fullName: function() {
      return this.firstName + " " + this.lastName;
    }
  };
});
