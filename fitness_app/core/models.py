from django.db import models


# -------------------------
# USER MODEL
# -------------------------
class User(models.Model):

    ROLE_CHOICES = (
        ('user', 'User'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin'),
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    password = models.CharField(
        max_length=100
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    specialization = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    experience = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    goal = models.CharField(
        max_length=100,
        default="Weight Loss"
    )

    def __str__(self):
        return self.email
    
    streak = models.IntegerField(
        default=0
    )

    longest_streak = models.IntegerField(
        default=0
    )

    last_streak_date = models.DateField(
        null=True,
        blank=True
    )


# -------------------------
# TRAINER MODEL
# -------------------------
class Trainer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    certificate = models.TextField()

    status = models.CharField(
        max_length=20,
        default="pending"
    )

    def __str__(self):
        return self.user.email


# -------------------------
# CHALLENGE MODEL
# -------------------------
class Challenge(models.Model):

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    days = models.CharField(max_length=50)

    image = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    category = models.CharField(max_length=50, default="General")

    def __str__(self):
        return self.name


# -------------------------
# USER JOIN CHALLENGE
# -------------------------
class JoinChallenge(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_date = models.DateField(
        null=True,
        blank=True
    )

    progress = models.IntegerField(
        default=0
    )

    def __str__(self):

        return f"{self.user.name} joined {self.challenge.name}"


# -------------------------
# REPORT MODEL
# -------------------------
class Report(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE
    )

    reason = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report on {self.challenge.name}"
    

class Activity(models.Model):

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.message
    
# -------------------------
# WEIGHT LOG MODEL
# -------------------------
class WeightLog(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    weight = models.FloatField()

    logged_date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):

        return f"""
        {self.user.name}
        - {self.weight} kg
        """
    
# -------------------------
# CALORIE LOG
# -------------------------
class CalorieLog(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    food_name = models.CharField(
        max_length=200
    )

    calories = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"""
        {self.user.name}
        - {self.food_name}
        """