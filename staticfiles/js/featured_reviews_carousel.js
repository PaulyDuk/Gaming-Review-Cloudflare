document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM loaded, initializing carousel...');
  
  const carouselElement = document.getElementById('featuredReviewsCarousel');
  
  if (carouselElement) {
    console.log('Carousel element found');
    
    // Make sure Bootstrap is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Carousel) {
      console.log('Bootstrap found, creating carousel');
      
      // Initialize carousel
      const carousel = new bootstrap.Carousel(carouselElement, {
        interval: 5000,
        wrap: true,
        keyboard: true,
        pause: 'hover'
      });
      
      console.log('Carousel initialized successfully');
      
      // Add event listeners for debugging
      carouselElement.addEventListener('slide.bs.carousel', function (e) {
        console.log('Carousel sliding from', e.from, 'to', e.to);
      });
      
      carouselElement.addEventListener('slid.bs.carousel', function (e) {
        console.log('Carousel slid to', e.to);
      });
      
    } else {
      console.error('Bootstrap not found or Carousel component not available');
    }
  } else {
    console.error('Carousel element with ID "featuredReviewsCarousel" not found');
  }
});
