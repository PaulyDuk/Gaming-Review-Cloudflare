from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.


class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)
    founded_year = models.IntegerField(blank=True, null=True)
    headquarters = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    logo = CloudinaryField('image', default='placeholder')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    founded_year = models.IntegerField(blank=True, null=True)
    headquarters = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    logo = CloudinaryField('image', default='placeholder')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('adventure', 'Adventure'),
        ('fighting', 'Fighting'),
        ('first-person shooter', 'First-Person Shooter'),
        ('horror', 'Horror'),
        ('indie', 'Indie'),
        ('platformer', 'Platformer'),
        ('puzzle', 'Puzzle'),
        ('racing', 'Racing'),
        ('role-playing', 'Role-Playing'),
        ('rpg', 'RPG'),
        ('shooter', 'Shooter'),
        ('simulation', 'Simulation'),
        ('sports', 'Sports'),
        ('strategy', 'Strategy'),
    ]

    CONSOLES = [
        ('Playstation', 'Playstation'),
        ('Playstation 2', 'Playstation 2'),
        ('Playstation 3', 'Playstation 3'),
        ('Playstation 4', 'Playstation 4'),
        ('Playstation 5', 'Playstation 5'),
        ('Nintendo 64', 'Nintendo 64'),
        ('Nintendo GameCube', 'Nintendo GameCube'),
        ('Nintendo Wii', 'Nintendo Wii'),
        ('Nintendo Wii U', 'Nintendo Wii U'),
        ('Nintendo Switch', 'Nintendo Switch'),
        ('Nintendo Switch 2', 'Nintendo Switch 2'),
        ('Xbox', 'Xbox'),
        ('Xbox 360', 'Xbox 360'),
        ('Xbox One', 'Xbox One'),
        ('Xbox Series X', 'Xbox Series X'),
        ('PC', 'PC'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name='reviews')
    developer = models.ForeignKey(
        Developer, on_delete=models.CASCADE, related_name='games')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    console = models.CharField(max_length=50, choices=CONSOLES, default='PC')
    description = models.TextField()
    release_date = models.DateField()

    # Review fields
    review_score = models.DecimalField(
        max_digits=3, decimal_places=1, blank=True, null=True)  # 0.0 to 10.0
    review_text = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    review_date = models.DateTimeField(blank=True, null=True)

    # Media
    featured_image = CloudinaryField('image', default='placeholder')

    # Metadata
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # User engagement
    likes = models.ManyToManyField(User, related_name='game_likes', blank=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        if self.review_score is not None:
            score_display = f"{self.review_score}/10"
        else:
            score_display = "No Score"
        return f"{self.title} | Score: {score_display}"

    def number_of_likes(self):
        return self.likes.count()
    

class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]
        verbose_name = 'User Comment'
        verbose_name_plural = 'User Comments'

    def __str__(self):
        review_title = self.review.title if self.review else "Unknown Review"
        return f"Comment by {self.author} on {review_title}"
