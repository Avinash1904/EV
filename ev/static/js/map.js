// Initialize and add the map
function initMap() {
    var locations = [
        ['Bondi Beach', -33.890542, 151.274856, 4],
        ['Coogee Beach', -33.923036, 151.259052, 5],
        ['Cronulla Beach', -34.028249, 151.157507, 3],
        ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
        ['Maroubra Beach', -33.950198, 151.259302, 1]
      ];

      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
        center: new google.maps.LatLng(-33.92, 151.25),
        mapTypeId: google.maps.MapTypeId.ROADMAP
      });

      var infowindow = new google.maps.InfoWindow();

      const svgMarker = {
        path: "M19,7h-0.82l-1.7,-4.68C16.19,1.53 15.44,1 14.6,1H12v2h2.6l1.46,4h-4.81l-0.36,-1H12V4H7v2h1.75l1.82,5H9.9C9.46,8.77 7.59,7.12 5.25,7.01C2.45,6.87 0,9.2 0,12c0,2.8 2.2,5 5,5c2.46,0 4.45,-1.69 4.9,-4h4.2c0.44,2.23 2.31,3.88 4.65,3.99c2.8,0.13 5.25,-2.19 5.25,-5C24,9.2 21.8,7 19,7zM7.82,13c-0.4,1.17 -1.49,2 -2.82,2c-1.68,0 -3,-1.32 -3,-3s1.32,-3 3,-3c1.33,0 2.42,0.83 2.82,2H5v2H7.82zM14.1,11h-1.4l-0.73,-2H15C14.56,9.58 14.24,10.25 14.1,11zM19,15c-1.68,0 -3,-1.32 -3,-3c0,-0.93 0.41,-1.73 1.05,-2.28l0.96,2.64l1.88,-0.68l-0.97,-2.67C18.94,9.01 18.97,9 19,9c1.68,0 3,1.32 3,3S20.68,15 19,15z",
        fillColor: "blue",
        fillOpacity: 0.6,
        strokeWeight: 0,
        rotation: 0,
        scale: 2,
        anchor: new google.maps.Point(15, 30),
      };

      var marker, i;

      for (i = 0; i < locations.length; i++) {
          const image =     "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";

        marker = new google.maps.Marker({
          position: new google.maps.LatLng(locations[i][1], locations[i][2]),
          map: map,
          icon: svgMarker
        });

        google.maps.event.addListener(marker, 'click', (function(marker, i) {
          return function() {
            infowindow.setContent(locations[i][0]);
            infowindow.open(map, marker);
          }
        })(marker, i));
      }


  }
