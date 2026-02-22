from datetime import date

DTYPE_MAPPING = {
    'title': str,
    'location': str,
    'latitude': float,
    'longitude': float,
    'description': str,
    'photo': str
}

CUSTOM_CARD_STYLING = """
<style>
.details-card {
    background: linear-gradient(135deg, #fff5f5 0%, #fff0f7 100%);
    border: 2px solid #ff6b8a;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(255, 107, 138, 0.2);
}
.details-card h2 {
    color: #d63384;
    margin-bottom: 10px;
}
.details-card p {
    color: #444;
}
</style>

"""

PLACEHOLDER_IMAGE_PATH = "married_aventino_key_hole.png"