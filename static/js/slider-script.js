$(document).ready(function() {
     $('.responsive').slick({
     dots: true,
     infinite: true,
     speed: 500,
     slidesToShow: 6,
     slidesToScroll: 1,
     responsive: [{
          breakpoint: 1024,
          settings: {
               slidesToShow: 6,
               slidesToScroll: 1,
               // centerMode: true,

          }

     }, {
          breakpoint: 800,
          settings: {
               slidesToShow: 3,
               slidesToScroll: 2,
               dots: true,
               infinite: true,

          }


     }, {
          breakpoint: 600,
          settings: {
               slidesToShow: 2,
               slidesToScroll: 2,
               dots: true,
               infinite: true,
               
          }
     }, {
          breakpoint: 480,
          settings: {
               slidesToShow: 1,
               slidesToScroll: 1,
               dots: true,
               infinite: true,
               autoplay: true,
               autoplaySpeed: 2000,
          }
     }]
     });


     });