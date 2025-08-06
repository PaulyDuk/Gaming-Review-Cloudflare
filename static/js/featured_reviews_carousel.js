document.addEventListener('DOMContentLoaded', function () {
  const carouselElement = document.getElementById('featuredReviewsCarousel');
  
  if (carouselElement) {
    // Make sure Bootstrap is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Carousel) {
      // Initialize carousel
      const carousel = new bootstrap.Carousel(carouselElement, {
        interval: 5000,
        wrap: true,
        keyboard: true,
        pause: 'hover'
      });
      
    } else {
      console.error('Bootstrap not found or Carousel component not available');
    }
  } else {
    console.error('Carousel element with ID "featuredReviewsCarousel" not found');
  }
});
