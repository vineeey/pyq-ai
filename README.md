# ULTIMATE ZERO-COST MASTER PROMPT — PYQ ANALYZER
## Complete Project Specification with SQLite3 & Llama 3.2 3B
---
> **COPY EVERYTHING BELOW THIS LINE AND GIVE TO YOUR AI ASSISTANT**
---
# MASTER PROMPT: PYQ ANALYZER — ZERO-COST EDITION
## ROLE & CONTEXT
You are an elite full-stack Django developer and AI engineer. You will build a complete, productionquality web application called **PYQ Analyzer** — an AI-powered Previous Year Question Paper
analysis system.
**Critical Constraints:**
- **Database**: SQLite3 only (no PostgreSQL, no external database)
- **LLM**: Ollama with Llama 3.2 3B model only (local, free, no API costs)
- **Embeddings**: sentence-transformers with all-MiniLM-L6-v2 (local, free)
- **Cost**: Absolute zero — no paid services, no API keys required
- **Frontend**: Award-winning UI using Tailwind CSS, Alpine.js, HTMX
- **Hosting**: Must work on free tiers (PythonAnywhere, Render, or local)
**Target System:**
- Minimum: 8GB RAM, any modern CPU, no GPU required
- Recommended: 16GB RAM for comfortable development
- Storage: 10GB free space minimum
---
## PROJECT OVERVIEW
### What We're Building
A web platform where users can:
1. Create subjects with custom module configurations
2. Upload previous year question paper PDFs
3. Define classification rules in plain English (converted to code by local LLM)
4. Get AI-powered analysis: module mapping, topic detection, duplicates, difficulty, Bloom's
taxonomy
5. View beautiful analytics dashboards
6. Download organized module-wise PDF reports
### Core Principle
**ZERO HARDCODING** — No specific exam board, university, or subject names hardcoded.
Everything is user-configurable through variables stored in the database.
### Design Philosophy
The UI must be **stunning and memorable** — inspired by:
- Linear. app (clean, minimal, powerful)
- Notion (warm, inviting, flexible)
- Stripe Dashboard (data-rich, professional)
- Vercel (dark mode excellence)
---
## TECHNOLOGY STACK
### Backend
```
Framework : Django 5. x
Python : 3. 11+
Database : SQLite3 (with WAL mode for better concurrency)
Task Queue : Django-Q2 (SQLite-based, no Redis needed)
 OR Huey (lightweight alternative)
```
### AI & ML (All Free, Local)
```
LLM : Ollama + Llama 3.2 3B (2GB RAM, runs on CPU)
Embeddings : sentence-transformers/all-MiniLM-L6-v2 (80MB model)
NLP : spaCy (en_core_web_sm model)
PDF Processing : pdfplumber + PyMuPDF + pytesseract
```
### Frontend
```
Templates : Django Templates
CSS : Tailwind CSS 3.x (CLI build, no Node runtime needed)
JavaScript : Alpine.js (15KB) + HTMX (14KB)
Charts : Chart.js
Icons : Lucide Icons (SVG, no external requests)
Animations : CSS animations + minimal GSAP
```
### Reports
```
PDF Generation : WeasyPrint (HTML → PDF)
Templating : Jinja2
```
---
## PROJECT STRUCTURE
```
pyq_analyzer/
├── config/ # Django project configuration
│ ├── __init__.py
│ ├── settings.py # Main settings (SQLite configured)
│ ├── urls.py # Root URL configuration
│ ├── wsgi.py
│ └── asgi.py
│
├── apps/ # Django applications
│ ├── core/ # Shared utilities, base models
│ │ ├── models.py # Abstract base models
│ │ ├── mixins.py # View mixins
│ │ ├── utils.py # Helper functions
│ │ ├── context_processors.py # Global template context
│ │ └── templatetags/ # Custom template tags
│ │
│ ├── users/ # Authentication & profiles
│ │ ├── models. py # Custom User model
│ │ ├── views.py # Auth views
│ │ ├── forms.py # Registration, login forms
│ │ └── urls.py
│ │
│ ├── subjects/ # Subject management
│ │ ├── models.py # Subject, Module config
│ │ ├── views. py # CRUD views
│ │ ├── forms.py
│ │ └── urls.py
│ │
│ ├── papers/ # PYQ upload & management
│ │ ├── models.py # Paper, upload tracking
│ │ ├── views. py # Upload, list, preview
│ │ ├── forms. py
│ │ └── urls.py
│ │
│ ├── questions/ # Extracted questions
│ │ ├── models.py # Question with all fields
│ │ ├── views.py # List, detail, edit
│ │ ├── forms. py
│ │ └── urls. py
│ │
│ ├── rules/ # User-defined classification rules
│ │ ├── models. py # Rule storage
│ │ ├── views. py # Rule editor
│ │ ├── forms. py
│ │ ├── compiler.py # LLM rule compilation
│ │ ├── executor.py # Safe rule execution
│ │ └── urls.py
│ │
│ ├── analysis/ # AI analysis engine
│ │ ├── services/
│ │ │ ├── extractor.py # PDF → questions
│ │ │ ├── classifier.py # Module classification
│ │ │ ├── embedder.py # Embedding generation
│ │ │ ├── similarity.py # Duplicate detection
│ │ │ ├── bloom.py # Bloom's taxonomy
│ │ │ └── difficulty.py # Difficulty estimation
│ │ ├── pipeline.py # Orchestration
│ │ ├── tasks.py # Background tasks
│ │ └── views.py
│ │
│ ├── analytics/ # Statistics & insights
│ │ ├── calculator.py # Stats computation
│ │ ├── views.py # Dashboard views
│ │ └── urls.py
│ │
│ └── reports/ # PDF report generation
│ ├── generator.py # Report builder
│ ├── templates/ # Report HTML templates
│ ├── views.py
│ └── urls.py
│
├── services/ # Core services (outside apps)
│ ├── llm/
│ │ ├── __init__. py
│ │ ├── ollama_client.py # Ollama API client
│ │ └── prompts.py # All LLM prompts
│ │
│ └── embedding/
│ ├── __init__.py
│ └── local_embedder.py # Sentence-transformers wrapper
│
├── templates/ # Global templates
│ ├── base/
│ │ ├── base.html # Master layout
│ │ ├── nav.html # Navigation
│ │ └── footer.html
│ ├── components/ # Reusable UI components
│ │ ├── button.html
│ │ ├── card.html
│ │ ├── modal.html
│ │ ├── table.html
│ │ ├── form_field.html
│ │ ├── alert.html
│ │ ├── badge.html
│ │ ├── dropdown.html
│ │ ├── tabs.html
│ │ ├── progress.html
│ │ ├── skeleton.html
│ │ ├── empty_state.html
│ │ └── stats_card.html
│ ├── pages/ # Full page templates
│ └── partials/ # HTMX partial responses
│
├── static/
│ ├── css/
│ │ ├── input.css # Tailwind input
│ │ └── output.css # Compiled CSS
│ ├── js/
│ │ ├── app.js # Main JS
│ │ └── components/ # Alpine components
│ └── images/
│
├── media/ # User uploads (dev)
│ ├── papers/ # Uploaded PDFs
│ ├── syllabi/ # Syllabus files
│ └── reports/ # Generated reports
│
├── db/ # Database directory
│ └── pyq_analyzer.sqlite3 # SQLite database file
│
├── tests/ # Test suite
├── docs/ # Documentation
├── scripts/ # Management scripts
│ ├── setup_ollama.sh # Ollama setup script
│ └── download_models.py # Download AI models
│
├── requirements.txt # Python dependencies
├── tailwind.config.js # Tailwind configuration
├── manage.py
├── . env.example
└── README.md
```
---
## DATABASE DESIGN (SQLite3)
### Configuration
```python
# config/settings.py
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
# SQLite3 Database Configuration
DATABASES = {
 'default': {
 'ENGINE': 'django.db.backends. sqlite3',
 'NAME': BASE_DIR / 'db' / 'pyq_analyzer.sqlite3',
 'OPTIONS': {
 'timeout': 30,
 },
 }
}
# Enable WAL mode for better concurrency (set via migration or signal)
# PRAGMA journal_mode=WAL;
# PRAGMA cache_size=-64000; # 64MB cache
# PRAGMA foreign_keys=ON;
```
### Model Specifications
#### BaseModel (Abstract)
```python
# apps/core/models.py
import uuid
from django. db import models
from django.utils import timezone
class BaseModel(models.Model):
 """Abstract base model with common fields"""

 id = models.UUIDField(
 primary_key=True,
 default=uuid.uuid4,
 editable=False
 )
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)

 class Meta:
 abstract = True
class SoftDeleteModel(BaseModel):
 """Base model with soft delete capability"""

 is_deleted = models. BooleanField(default=False)
 deleted_at = models.DateTimeField(null=True, blank=True)

 class Meta:
 abstract = True

 def soft_delete(self):
 self.is_deleted = True
 self. deleted_at = timezone.now()
 self.save(update_fields=['is_deleted', 'deleted_at'])

 def restore(self):
 self.is_deleted = False
 self.deleted_at = None
 self. save(update_fields=['is_deleted', 'deleted_at'])
```
#### User Model
```python
# apps/users/models.py
from django.contrib. auth.models import AbstractUser
from django. db import models
from apps.core.models import BaseModel
import json
class User(AbstractUser):
 """Extended User model"""

 id = models.UUIDField(
 primary_key=True,
 default=uuid.uuid4,
 editable=False
 )
 email = models.EmailField(unique=True)
 full_name = models. CharField(max_length=255, blank=True)
 avatar = models. ImageField(
 upload_to='avatars/',
 null=True,
 blank=True
 )
 institution = models.CharField(max_length=255, blank=True)

 # Preferences stored as JSON
 preferences = models.JSONField(default=dict, blank=True)
 # Example: {"theme": "dark", "notifications": true}

 created_at = models. DateTimeField(auto_now_add=True)
 updated_at = models. DateTimeField(auto_now=True)

 USERNAME_FIELD = 'email'
 REQUIRED_FIELDS = ['username']

 class Meta:
 db_table = 'users'

 def __str__(self):
 return self.email

 @property
 def theme(self):
 return self.preferences. get('theme', 'light')

 @theme. setter
 def theme(self, value):
 self.preferences['theme'] = value
 self.save(update_fields=['preferences'])
```
#### Subject Model
```python
# apps/subjects/models.py
from django.db import models
from apps. core.models import SoftDeleteModel
from apps.users.models import User
import json
class Subject(SoftDeleteModel):
 """Subject with configurable modules"""

 # Basic Info
 code = models.CharField(max_length=50)
 name = models.CharField(max_length=255)
 description = models.TextField(blank=True)
 scheme_year = models.CharField(
 max_length=20,
 help_text="e.g., 2019, 2021-2022"
 )

 # Module Configuration
 num_modules = models. PositiveIntegerField(
 default=5,
 help_text="Number of modules (1-20)"
 )

 # Module details stored as JSON array
 # [{"index": 1, "name": "Module 1", "description": ".. .", "topics": ["Topic A", "Topic B"]}, ...]
 module_config = models.JSONField(default=list, blank=True)

 # Exam pattern (optional default mapping)
 # {"1-5": 1, "6-10": 2, ... } means Q1-5 → Module 1, Q6-10 → Module 2
 exam_pattern = models. JSONField(default=dict, blank=True)

 # Subject-level settings
 # {"ocr_enabled": true, "similarity_threshold": 0.85, ...}
 settings = models.JSONField(default=dict, blank=True)

 # Ownership
 owner = models.ForeignKey(
 User,
 on_delete=models.CASCADE,
 related_name='owned_subjects'
 )

 # Denormalized counts for performance
 papers_count = models. PositiveIntegerField(default=0)
 questions_count = models. PositiveIntegerField(default=0)

 # Status
 is_archived = models.BooleanField(default=False)
 last_analyzed_at = models.DateTimeField(null=True, blank=True)

 class Meta:
 db_table = 'subjects'
 unique_together = ['owner', 'code']
 ordering = ['-created_at']

 def __str__(self):
 return f"{self.code} - {self. name}"

 def get_module_name(self, index):
 """Get module name by index (1-based)"""
 for module in self.module_config:
 if module.get('index') == index:
 return module. get('name', f'Module {index}')
 return f'Module {index}'

 def get_module_topics(self, index):
 """Get topics for a module"""
 for module in self.module_config:
 if module.get('index') == index:
 return module. get('topics', [])
 return []

 def initialize_modules(self):
 """Initialize module_config with default structure"""
 if not self.module_config:
 self. module_config = [
 {
 "index": i,
 "name": f"Module {i}",
 "description": "",
 "topics": []
 }
 for i in range(1, self.num_modules + 1)
 ]
 self.save(update_fields=['module_config'])
```
#### Syllabus Model
```python
# apps/subjects/models.py (continued)
class Syllabus(models.Model):
 """Syllabus for a subject"""

 id = models.UUIDField(
 primary_key=True,
 default=uuid.uuid4,
 editable=False
 )
 subject = models.OneToOneField(
 Subject,
 on_delete=models.CASCADE,
 related_name='syllabus'
 )

 # File or text input
 file = models.FileField(
 upload_to='syllabi/',
 null=True,
 blank=True
 )
 file_name = models.CharField(max_length=255, blank=True)

 # Extracted content
 raw_text = models.TextField(blank=True)

 # Module-wise extracted text as JSON array
 # [{"index": 1, "content": "..."}, ...]
 module_texts = models.JSONField(default=list, blank=True)

 # AI-extracted topics per module
 # [{"index": 1, "topics": [{"name": ".. .", "keywords": [... ]}]}, ...]
 topics_extracted = models.JSONField(default=list, blank=True)

 # Processing status
 STATUS_CHOICES = [
 ('pending', 'Pending'),
 ('processing', 'Processing'),
 ('completed', 'Completed'),
 ('failed', 'Failed'),
 ]
 processing_status = models. CharField(
 max_length=20,
 choices=STATUS_CHOICES,
 default='pending'
 )
 processing_error = models. TextField(blank=True)

 # Timestamps
 processed_at = models. DateTimeField(null=True, blank=True)
 created_at = models. DateTimeField(auto_now_add=True)
 updated_at = models. DateTimeField(auto_now=True)

 class Meta:
 db_table = 'syllabi'

 def __str__(self):
 return f"Syllabus for {self.subject. code}"
```
#### Paper Model
```python
# apps/papers/models.py
from django.db import models
from apps.core.models import BaseModel
from apps. subjects.models import Subject
from apps.users. models import User
class Paper(BaseModel):
 """Uploaded question paper"""

 subject = models.ForeignKey(
 Subject,
 on_delete=models. CASCADE,
 related_name='papers'
 )

 # File info
 file = models.FileField(upload_to='papers/')
 file_name = models.CharField(max_length=255)
 file_size = models. PositiveIntegerField(help_text="Size in bytes")

 # Metadata
 year_label = models.CharField(
 max_length=100,
 help_text="e. g., December 2023, 2022 Supplementary"
 )
 exam_type = models. CharField(
 max_length=100,
 blank=True,
 help_text="Regular, Supplementary, Model, etc."
 )
 exam_date = models. DateField(null=True, blank=True)
 total_pages = models. PositiveIntegerField(default=0)

 # Additional metadata as JSON
 metadata = models.JSONField(default=dict, blank=True)

 # Processing status
 STATUS_CHOICES = [
 ('uploaded', 'Uploaded'),
 ('extracting', 'Extracting Questions'),
 ('extracted', 'Questions Extracted'),
 ('classifying', 'Classifying'),
 ('completed', 'Completed'),
 ('failed', 'Failed'),
 ]
 processing_status = models.CharField(
 max_length=20,
 choices=STATUS_CHOICES,
 default='uploaded'
 )
 processing_error = models. TextField(blank=True)
 processing_started_at = models. DateTimeField(null=True, blank=True)
 processing_completed_at = models.DateTimeField(null=True, blank=True)

 # Denormalized count
 questions_count = models.PositiveIntegerField(default=0)

 # Tracking
 uploaded_by = models.ForeignKey(
 User,
 on_delete=models. SET_NULL,
 null=True,
 related_name='uploaded_papers'
 )

 class Meta:
 db_table = 'papers'
 ordering = ['-year_label', '-created_at']
 indexes = [
 models.Index(fields=['subject', 'year_label']),
 models.Index(fields=['processing_status']),
 ]

 def __str__(self):
 return f"{self.subject.code} - {self.year_label}"
```
#### Question Model
```python
# apps/questions/models. py
from django. db import models
from apps.core.models import BaseModel
from apps. papers.models import Paper
from apps.subjects. models import Subject
from apps.users.models import User
import json
class Question(BaseModel):
 """Extracted question with all analysis fields"""

 # Relationships
 paper = models.ForeignKey(
 Paper,
 on_delete=models.CASCADE,
 related_name='questions'
 )
 subject = models.ForeignKey(
 Subject,
 on_delete=models. CASCADE,
 related_name='questions'
 ) # Denormalized for query efficiency

 # === EXTRACTION DATA ===
 question_number = models.CharField(
 max_length=20,
 help_text="e. g., 1, 2a, 11. i"
 )
 question_number_numeric = models.PositiveIntegerField(
 null=True,
 blank=True,
 help_text="Numeric part for sorting"
 )
 question_text = models. TextField()
 question_text_clean = models.TextField(
 blank=True,
 help_text="Normalized, lowercased for matching"
 )

 part = models.CharField(
 max_length=10,
 blank=True,
 help_text="A, B, Part 1, Part 2, etc."
 )
 sub_part = models. CharField(
 max_length=10,
 blank=True,
 help_text="a, b, i, ii, etc."
 )

 marks = models.DecimalField(
 max_digits=5,
 decimal_places=2,
 null=True,
 blank=True
 )
 marks_text = models.CharField(
 max_length=50,
 blank=True,
 help_text="Original marks text like '2x5=10'"
 )

 page_number = models. PositiveIntegerField(default=1)

 # Diagram/Image handling
 has_diagram = models. BooleanField(default=False)
 has_table = models.BooleanField(default=False)
 has_equation = models.BooleanField(default=False)
 diagram_image = models.ImageField(
 upload_to='diagrams/',
 null=True,
 blank=True
 )

 extraction_confidence = models.FloatField(
 default=1.0,
 help_text="0.0 to 1.0"
 )

 # === CLASSIFICATION - RULE BASED ===
 module_by_rule = models. PositiveIntegerField(
 null=True,
 blank=True,
 help_text="Module assigned by user rule"
 )
 rule_matched = models.ForeignKey(
 'rules.Rule',
 on_delete=models. SET_NULL,
 null=True,
 blank=True,
 related_name='matched_questions'
 )
 rule_match_details = models.JSONField(
 default=dict,
 blank=True
 )

 # === CLASSIFICATION - PATTERN BASED ===
 module_by_pattern = models.PositiveIntegerField(
 null=True,
 blank=True,
 help_text="Module assigned by exam pattern"
 )
 pattern_match_details = models. JSONField(
 default=dict,
 blank=True
 )

 # === CLASSIFICATION - AI BASED ===
 module_by_ai = models.PositiveIntegerField(
 null=True,
 blank=True,
 help_text="Module assigned by AI"
 )
 ai_confidence = models.FloatField(
 null=True,
 blank=True,
 help_text="0.0 to 1.0"
 )
 ai_reasoning = models.TextField(
 blank=True,
 help_text="LLM explanation"
 )

 # === FINAL CLASSIFICATION ===
 CLASSIFICATION_METHOD_CHOICES = [
 ('rule', 'Rule-based'),
 ('pattern', 'Pattern-based'),
 ('ai', 'AI-based'),
 ('manual', 'Manual'),
 ('unclassified', 'Unclassified'),
 ]
 module_final = models.PositiveIntegerField(
 null=True,
 blank=True
 )
 classification_method = models. CharField(
 max_length=20,
 choices=CLASSIFICATION_METHOD_CHOICES,
 default='unclassified'
 )

 # Manual verification
 is_manually_verified = models. BooleanField(default=False)
 verified_by = models. ForeignKey(
 User,
 on_delete=models.SET_NULL,
 null=True,
 blank=True,
 related_name='verified_questions'
 )
 verified_at = models. DateTimeField(null=True, blank=True)

 # === TOPIC MAPPING ===
 topic_primary = models.CharField(max_length=255, blank=True)
 topic_secondary = models.JSONField(
 default=list,
 blank=True
 ) # Array of strings
 topic_confidence = models.FloatField(
 null=True,
 blank=True
 )

 # === BLOOM'S TAXONOMY ===
 BLOOM_LEVEL_CHOICES = [
 ('remember', 'Remember'),
 ('understand', 'Understand'),
 ('apply', 'Apply'),
 ('analyze', 'Analyze'),
 ('evaluate', 'Evaluate'),
 ('create', 'Create'),
 ]
 bloom_level = models.CharField(
 max_length=20,
 choices=BLOOM_LEVEL_CHOICES,
 blank=True
 )
 bloom_confidence = models.FloatField(
 null=True,
 blank=True
 )
 bloom_indicators = models.JSONField(
 default=dict,
 blank=True
 ) # {"verbs": ["explain", "describe"], "reasoning": "..."}

 # === DIFFICULTY ===
 DIFFICULTY_CHOICES = [
 ('easy', 'Easy'),
 ('medium', 'Medium'),
 ('hard', 'Hard'),
 ]
 difficulty = models.CharField(
 max_length=20,
 choices=DIFFICULTY_CHOICES,
 blank=True
 )
 difficulty_score = models.FloatField(
 null=True,
 blank=True,
 help_text="0.0 to 1.0"
 )
 difficulty_factors = models.JSONField(
 default=dict,
 blank=True
 )

 # === EMBEDDING (stored as JSON for SQLite) ===
 embedding = models.JSONField(
 null=True,
 blank=True,
 help_text="384-dim vector as JSON array"
 )
 embedding_model = models.CharField(
 max_length=100,
 blank=True,
 default='all-MiniLM-L6-v2'
 )
 embedded_at = models.DateTimeField(null=True, blank=True)

 # === CLUSTERING ===
 cluster = models.ForeignKey(
 'QuestionCluster',
 on_delete=models.SET_NULL,
 null=True,
 blank=True,
 related_name='questions'
 )
 cluster_similarity = models.FloatField(
 null=True,
 blank=True
 )

 # === METADATA ===
 flags = models.JSONField(
 default=dict,
 blank=True
 ) # Any issues, notes

 class Meta:
 db_table = 'questions'
 ordering = ['question_number_numeric', 'question_number']
 indexes = [
 models. Index(fields=['subject', 'module_final']),
 models.Index(fields=['paper']),
 models.Index(fields=['subject', 'topic_primary']),
 ]

 def __str__(self):
 return f"Q{self.question_number} - {self.paper.year_label}"

 def save(self, *args, **kwargs):
 # Auto-generate clean text
 if self.question_text and not self.question_text_clean:
 self.question_text_clean = self.question_text. lower(). strip()

 # Extract numeric part of question number
 if self. question_number and not self.question_number_numeric:
 import re
 match = re.search(r'\d+', self.question_number)
 if match:
 self.question_number_numeric = int(match.group())

 super().save(*args, **kwargs)
class QuestionCluster(BaseModel):
 """Group of similar/duplicate questions"""

 subject = models.ForeignKey(
 Subject,
 on_delete=models. CASCADE,
 related_name='clusters'
 )

 CLUSTER_TYPE_CHOICES = [
 ('duplicate', 'Duplicate'),
 ('similar', 'Similar'),
 ('thematic', 'Thematic'),
 ]
 cluster_type = models. CharField(
 max_length=20,
 choices=CLUSTER_TYPE_CHOICES,
 default='similar'
 )

 representative_text = models.TextField(
 blank=True,
 help_text="Canonical form of the question"
 )
 representative_question = models.ForeignKey(
 Question,
 on_delete=models.SET_NULL,
 null=True,
 blank=True,
 related_name='represented_clusters'
 )

 question_count = models. PositiveIntegerField(default=0)
 years_appeared = models.JSONField(default=list) # Array of year labels

 min_similarity = models.FloatField(default=0.0)
 avg_similarity = models. FloatField(default=0.0)

 is_evergreen = models.BooleanField(
 default=False,
 help_text="Appears frequently across years"
 )
 importance_score = models. FloatField(default=0.0)

 class Meta:
 db_table = 'question_clusters'
 ordering = ['-importance_score', '-question_count']
```
#### Rule Model
```python
# apps/rules/models.py
from django.db import models
from apps.core. models import BaseModel
from apps.subjects. models import Subject
from apps.users.models import User
class Rule(BaseModel):
 """User-defined classification rule"""

 subject = models.ForeignKey(
 Subject,
 on_delete=models. CASCADE,
 related_name='rules'
 )

 # Rule identification
 name = models.CharField(max_length=255)
 description = models.TextField(blank=True)

 # User's natural language rule
 rule_text = models. TextField(
 help_text="Plain English rule, e.g., 'Q1-5 belong to Module 1'"
 )

 # LLM-parsed structured format
 parsed_rule = models. JSONField(
 default=dict,
 blank=True,
 help_text="Structured JSON from LLM parsing"
 )
 # Example:
 # {
 # "conditions": {
 # "question_numbers": [1, 2, 3, 4, 5],
 # "question_ranges": [[1, 5]],
 # "keywords": ["fourier", "laplace"],
 # "marks": [2, 5],
 # "parts": ["A"]
 # },
 # "action": {"module": 1}
 # }

 # LLM-generated Python function (as string)
 generated_code = models.TextField(
 blank=True,
 help_text="Python function generated by LLM"
 )

 # Validation
 code_validated = models.BooleanField(default=False)
 validation_errors = models. JSONField(default=list, blank=True)

 # Execution order (lower = higher priority)
 priority = models. PositiveIntegerField(
 default=100,
 help_text="Lower number = higher priority"
 )

 # Status
 is_enabled = models.BooleanField(default=True)

 # Statistics
 match_count = models. PositiveIntegerField(
 default=0,
 help_text="Number of questions matched"
 )
 last_matched_at = models. DateTimeField(null=True, blank=True)

 # Tracking
 created_by = models.ForeignKey(
 User,
 on_delete=models. SET_NULL,
 null=True,
 related_name='created_rules'
 )

 class Meta:
 db_table = 'rules'
 ordering = ['priority', 'created_at']
 indexes = [
 models.Index(fields=['subject', 'is_enabled', 'priority']),
 ]

 def __str__(self):
 return f"{self.name} ({self.subject.code})"
```
#### Analytics Models
```python
# apps/analytics/models.py
from django.db import models
from apps.core. models import BaseModel
from apps.subjects. models import Subject
from apps.users.models import User
class AnalysisSnapshot(BaseModel):
 """Snapshot of analysis results"""

 subject = models.ForeignKey(
 Subject,
 on_delete=models.CASCADE,
 related_name='analysis_snapshots'
 )

 ANALYSIS_TYPE_CHOICES = [
 ('full', 'Full Analysis'),
 ('incremental', 'Incremental'),
 ('manual', 'Manual Trigger'),
 ]
 analysis_type = models.CharField(
 max_length=20,
 choices=ANALYSIS_TYPE_CHOICES,
 default='full'
 )

 triggered_by = models. ForeignKey(
 User,
 on_delete=models.SET_NULL,
 null=True
 )

 STATUS_CHOICES = [
 ('pending', 'Pending'),
 ('running', 'Running'),
 ('completed', 'Completed'),
 ('failed', 'Failed'),
 ]
 status = models.CharField(
 max_length=20,
 choices=STATUS_CHOICES,
 default='pending'
 )

 started_at = models. DateTimeField(null=True, blank=True)
 completed_at = models. DateTimeField(null=True, blank=True)
 duration_seconds = models. PositiveIntegerField(default=0)

 # Counts
 papers_analyzed = models.PositiveIntegerField(default=0)
 questions_analyzed = models.PositiveIntegerField(default=0)

 # Results stored as JSON
 results_summary = models.JSONField(default=dict, blank=True)
 # Example:
 # {
 # "modules": {"1": {"count": 50, "avg_marks": 5.2}, ... },
 # "topics": {"Topic A": {"count": 20, "frequency": 0.4}, ...},
 # "difficulty": {"easy": 30, "medium": 50, "hard": 20},
 # "bloom": {"remember": 25, "understand": 35, ... }
 # }

 detailed_results = models. JSONField(default=dict, blank=True)
 errors = models.JSONField(default=list, blank=True)

 class Meta:
 db_table = 'analysis_snapshots'
 ordering = ['-created_at']
class Report(BaseModel):
 """Generated report"""

 subject = models.ForeignKey(
 Subject,
 on_delete=models. CASCADE,
 related_name='reports'
 )

 REPORT_TYPE_CHOICES = [
 ('module', 'Module Report'),
 ('full_subject', 'Full Subject Report'),
 ('topic', 'Topic Report'),
 ('trend', 'Trend Report'),
 ('custom', 'Custom Report'),
 ]
 report_type = models.CharField(
 max_length=20,
 choices=REPORT_TYPE_CHOICES
 )

 module_index = models.PositiveIntegerField(
 null=True,
 blank=True,
 help_text="For module-specific reports"
 )

 title = models.CharField(max_length=255)

 # Report configuration
 configuration = models.JSONField(
 default=dict,
 blank=True
 )
 # Example:
 # {
 # "include_analytics": true,
 # "include_diagrams": true,
 # "group_by_topic": true,
 # "years_filter": ["2022", "2023"]
 # }

 # Generated file
 generated_file = models. FileField(
 upload_to='reports/',
 null=True,
 blank=True
 )
 file_format = models.CharField(
 max_length=10,
 default='pdf'
 )
 file_size = models. PositiveIntegerField(default=0)

 # Generation status
 STATUS_CHOICES = [
 ('pending', 'Pending'),
 ('generating', 'Generating'),
 ('completed', 'Completed'),
 ('failed', 'Failed'),
 ]
 generation_status = models. CharField(
 max_length=20,
 choices=STATUS_CHOICES,
 default='pending'
 )
 generation_error = models. TextField(blank=True)

 generated_by = models.ForeignKey(
 User,
 on_delete=models. SET_NULL,
 null=True
 )
 generated_at = models. DateTimeField(null=True, blank=True)

 download_count = models.PositiveIntegerField(default=0)

 class Meta:
 db_table = 'reports'
 ordering = ['-created_at']
```
---
## OLLAMA + LLAMA 3. 2 3B INTEGRATION
### Ollama Setup Script
```bash
#!/bin/bash
# scripts/setup_ollama.sh
echo " Setting up Ollama with Llama 3. 2 3B..."
# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
 echo " Installing Ollama..."
 curl -fsSL https://ollama.com/install. sh | sh
else
 echo "✅Ollama already installed"
fi
# Start Ollama service (if not running)
echo " Starting Ollama service..."
ollama serve &
sleep 5
# Pull Llama 3. 2 3B model
echo " Downloading Llama 3.2 3B model (this may take a few minutes)..."
ollama pull llama3.2:3b
# Verify installation
echo " Verifying installation..."
ollama list
echo "✅Setup complete! Ollama is ready with Llama 3.2 3B"
echo " RAM Usage: ~2-2.5 GB when model is loaded"
echo " API Endpoint: http://localhost:11434"
```
### Ollama Client
```python
# services/llm/ollama_client.py
import requests
import json
import logging
from typing import Optional, Dict, Any, List
from django.conf import settings
logger = logging.getLogger(__name__)
class OllamaClient:
 """
 Client for Ollama local LLM server.
 Configured for Llama 3.2 3B model.
 """

 def __init__(self):
 self.base_url = getattr(
 settings,
 'OLLAMA_BASE_URL',
 'http://localhost:11434'
 )
 self.default_model = getattr(
 settings,
 'OLLAMA_MODEL',
 'llama3.2:3b'
 )
 self.timeout = getattr(
 settings,
 'OLLAMA_TIMEOUT',
 120 # 2 minutes for slow CPUs
 )

 def is_available(self) -> bool:
 """Check if Ollama server is running and model is available."""
 try:
 response = requests. get(
 f"{self.base_url}/api/tags",
 timeout=5
 )
 if response.status_code == 200:
 models = response.json(). get('models', [])
 model_names = [m['name'] for m in models]
 return any(
 self.default_model in name
 for name in model_names
 )
 return False
 except requests.exceptions.RequestException:
 return False

 def generate(
 self,
 prompt: str,
 system: Optional[str] = None,
 model: Optional[str] = None,
 temperature: float = 0.7,
 max_tokens: int = 2000,
 stream: bool = False
 ) -> str:
 """
 Generate text completion from prompt.

 Args:
 prompt: The user prompt
 system: System message to set context
 model: Model to use (defaults to llama3.2:3b)
 temperature: Creativity (0.0-1.0)
 max_tokens: Maximum tokens to generate
 stream: Whether to stream response

 Returns:
 Generated text string
 """
 model = model or self.default_model

 payload = {
 "model": model,
 "prompt": prompt,
 "stream": stream,
 "options": {
 "temperature": temperature,
 "num_predict": max_tokens,
 }
 }

 if system:
 payload["system"] = system

 try:
 logger.debug(f"Ollama request: model={model}, prompt_len={len(prompt)}")

 response = requests. post(
 f"{self.base_url}/api/generate",
 json=payload,
 timeout=self.timeout
 )
 response.raise_for_status()

 result = response.json()
 generated_text = result. get("response", "")

 logger. debug(f"Ollama response: len={len(generated_text)}")
 return generated_text

 except requests.exceptions.ConnectionError:
 logger.error("Cannot connect to Ollama server")
 raise OllamaConnectionError(
 "Cannot connect to Ollama. "
 "Make sure it's running with: ollama serve"
 )
 except requests.exceptions. Timeout:
 logger.error("Ollama request timed out")
 raise OllamaTimeoutError(
 f"Request timed out after {self.timeout}s. "
 "The model might be loading or prompt too complex."
 )
 except requests.exceptions.HTTPError as e:
 logger.error(f"Ollama HTTP error: {e}")
 raise OllamaError(f"HTTP error: {e}")

 def generate_json(
 self,
 prompt: str,
 system: Optional[str] = None,
 model: Optional[str] = None
 ) -> Dict[str, Any]:
 """
 Generate and parse JSON response.

 Uses lower temperature for consistent JSON output.
 Handles common JSON extraction from markdown code blocks.
 """
 default_system = (
 "You are a helpful assistant. "
 "Always respond with valid JSON only. "
 "Do not include any text before or after the JSON. "
 "Do not wrap the JSON in markdown code blocks."
 )

 response = self.generate(
 prompt=prompt,
 system=system or default_system,
 model=model,
 temperature=0.3, # Lower for consistent output
 )

 return self._parse_json_response(response)

 def _parse_json_response(self, response: str) -> Dict[str, Any]:
 """Extract and parse JSON from response text."""
 text = response.strip()

 # Try direct parsing first
 try:
 return json. loads(text)
 except json.JSONDecodeError:
 pass

 # Try extracting from markdown code blocks
 if "```json" in text:
 try:
 json_str = text.split("```json")[1]. split("```")[0]
 return json.loads(json_str. strip())
 except (IndexError, json.JSONDecodeError):
 pass

 if "```" in text:
 try:
 json_str = text.split("```")[1].split("```")[0]
 return json. loads(json_str.strip())
 except (IndexError, json.JSONDecodeError):
 pass

 # Try finding JSON object in text
 try:
 start = text.index('{')
 end = text.rindex('}') + 1
 json_str = text[start:end]
 return json. loads(json_str)
 except (ValueError, json.JSONDecodeError):
 pass

 # Try finding JSON array in text
 try:
 start = text.index('[')
 end = text.rindex(']') + 1
 json_str = text[start:end]
 return json.loads(json_str)
 except (ValueError, json.JSONDecodeError):
 pass

 raise OllamaParseError(
 f"Failed to parse JSON from response: {text[:200]}..."
 )

 def chat(
 self,
 messages: List[Dict[str, str]],
 model: Optional[str] = None,
 temperature: float = 0.7
 ) -> str:
 """
 Chat completion with message history.

 Args:
 messages: List of {"role": "user"|"assistant", "content": "..."}
 model: Model to use
 temperature: Creativity level
 """
 model = model or self.default_model

 payload = {
 "model": model,
 "messages": messages,
 "stream": False,
 "options": {
 "temperature": temperature,
 }
 }

 try:
 response = requests.post(
 f"{self.base_url}/api/chat",
 json=payload,
 timeout=self.timeout
 )
 response. raise_for_status()

 result = response.json()
 return result.get("message", {}).get("content", "")

 except requests.exceptions.RequestException as e:
 logger.error(f"Ollama chat error: {e}")
 raise OllamaError(f"Chat request failed: {e}")

 def list_models(self) -> List[str]:
 """List available models."""
 try:
 response = requests.get(
 f"{self. base_url}/api/tags",
 timeout=10
 )
 response.raise_for_status()
 models = response.json(). get('models', [])
 return [m['name'] for m in models]
 except requests.exceptions.RequestException:
 return []
# Custom exceptions
class OllamaError(Exception):
 """Base exception for Ollama errors."""
 pass
class OllamaConnectionError(OllamaError):
 """Raised when cannot connect to Ollama server."""
 pass
class OllamaTimeoutError(OllamaError):
 """Raised when request times out."""
 pass
class OllamaParseError(OllamaError):
 """Raised when cannot parse LLM response."""
 pass
# Singleton instance
_client = None
def get_ollama_client() -> OllamaClient:
 """Get singleton Ollama client instance."""
 global _client
 if _client is None:
 _client = OllamaClient()
 return _client
```
### LLM Prompts
```python
# services/llm/prompts.py
"""
All LLM prompts for PYQ Analyzer.
Optimized for Llama 3.2 3B model.
"""
# ============================================================
# RULE COMPILATION PROMPT
# ============================================================
RULE_COMPILATION_SYSTEM = """You are a rule compiler that converts natural language
classification rules into structured JSON.
You will receive:
1. Subject information (name, number of modules)
2. User-written rules in plain English
You must output ONLY valid JSON with this structure:
{
 "rules": [
 {
 "id": "unique_snake_case_id",
 "name": "Human Readable Name",
 "original_text": "The original rule text",
 "priority": 1,
 "conditions": {
 "question_numbers": [1, 2, 3] or null,
 "question_ranges": [[1, 5], [10, 15]] or null,
 "parts": ["A", "B"] or null,
 "marks": [2, 5] or null,
 "keywords": ["keyword1", "keyword2"] or null,
 "has_diagram": true/false or null
 },
 "action": {
 "module": 1
 }
 }
 ],
 "errors": [],
 "warnings": []
}
Important:
- Module numbers must be between 1 and the given num_modules
- Parse question ranges like "Q1-5" as [[1, 5]]
- Parse lists like "Q1, 2, 3" as [1, 2, 3]
- Keywords should be lowercase
- If a rule is ambiguous, add to warnings
- If a rule cannot be parsed, add to errors and skip it"""
RULE_COMPILATION_TEMPLATE = """Subject: {subject_name}
Number of Modules: {num_modules}
Module Names: {module_names}
User Rules:
{user_rules}
Convert these rules to JSON format. Output ONLY the JSON, nothing else."""
# ============================================================
# MODULE CLASSIFICATION PROMPT
# ============================================================
MODULE_CLASSIFICATION_SYSTEM = """You are an academic question classifier. Given a question
and module descriptions, determine which module the question belongs to.
Output ONLY valid JSON:
{
 "module": 1,
 "confidence": 0.85,
 "reasoning": "Brief explanation"
}
Important:
- Module must be a number between 1 and num_modules
- Confidence is 0.0 to 1.0 (1.0 = very confident)
- Keep reasoning under 50 words"""
MODULE_CLASSIFICATION_TEMPLATE = """Question: {question_text}
Marks: {marks}
Available Modules:
{modules_description}
Which module does this question belong to? Output JSON only."""
# ============================================================
# QUESTION EXTRACTION PROMPT
# ============================================================
QUESTION_EXTRACTION_SYSTEM = """You are an exam paper parser. Extract individual questions
from the given text.
Output ONLY valid JSON:
{
 "questions": [
 {
 "number": "1",
 "text": "Full question text",
 "part": "A" or null,
 "marks": 5 or null,
 "has_diagram_reference": false
 }
 ]
}
Important:
- Preserve question numbers exactly (1, 2a, 3. i, etc.)
- Extract marks if visible (in parentheses, brackets, etc.)
- Set has_diagram_reference to true if question mentions "figure", "diagram", etc.
- Keep question text complete but clean"""
QUESTION_EXTRACTION_TEMPLATE = """Extract questions from this exam paper text:
---
{page_text}
---
Output JSON only."""
# ============================================================
# TOPIC EXTRACTION PROMPT
# ============================================================
TOPIC_EXTRACTION_SYSTEM = """You are an academic topic identifier. Given a question, identify
the main topic it covers.
Output ONLY valid JSON:
{
 "primary_topic": "Topic Name",
 "keywords": ["keyword1", "keyword2"],
 "confidence": 0.8
}
Keep topic names concise (2-5 words)."""
TOPIC_EXTRACTION_TEMPLATE = """Question: {question_text}
Subject: {subject_name}
Module: {module_name}
Known topics in this module: {known_topics}
Identify the topic. Output JSON only."""
# ============================================================
# SYLLABUS PARSING PROMPT
# ============================================================
SYLLABUS_PARSING_SYSTEM = """You are a syllabus parser. Extract module-wise content and topics
from syllabus text.
Output ONLY valid JSON:
{
 "modules": [
 {
 "index": 1,
 "name": "Module Name",
 "topics": [
 {"name": "Topic 1", "keywords": ["kw1", "kw2"]},
 {"name": "Topic 2", "keywords": ["kw3"]}
 ]
 }
 ]
}"""
SYLLABUS_PARSING_TEMPLATE = """Parse this syllabus into {num_modules} modules:
---
{syllabus_text}
---
Output JSON only."""
# ============================================================
# BLOOM'S TAXONOMY PROMPT (for complex cases)
# ============================================================
BLOOM_CLASSIFICATION_SYSTEM = """You are a Bloom's Taxonomy classifier. Classify the cognitive
level of academic questions.
Levels (low to high):
1. Remember - recall facts, define terms
2. Understand - explain, describe, summarize
3. Apply - use knowledge, solve problems, calculate
4. Analyze - examine, compare, differentiate
5. Evaluate - judge, justify, critique
6. Create - design, develop, propose
Output ONLY valid JSON:
{
 "level": "understand",
 "confidence": 0.9,
 "indicator_verbs": ["explain", "describe"]
}"""
BLOOM_CLASSIFICATION_TEMPLATE = """Classify this question's cognitive level:
Question: {question_text}
Output JSON only."""
# ============================================================
# DIFFICULTY ESTIMATION PROMPT (for complex cases)
# ============================================================
DIFFICULTY_ESTIMATION_SYSTEM = """You are an academic difficulty estimator. Estimate question
difficulty.
Output ONLY valid JSON:
{
 "difficulty": "medium",
 "score": 0.6,
 "factors": ["requires multiple concepts", "moderate length"]
}
difficulty must be: "easy", "medium", or "hard"
score is 0.0 (easiest) to 1.0 (hardest)"""
DIFFICULTY_ESTIMATION_TEMPLATE = """Estimate difficulty:
Question: {question_text}
Marks: {marks}
Bloom Level: {bloom_level}
Output JSON only."""
# ============================================================
# Helper function to format prompts
# ============================================================
def format_prompt(template: str, **kwargs) -> str:
 """Format a prompt template with given values."""
 return template.format(**kwargs)
```
### Rule Compiler Service
```python
# apps/rules/compiler.py
import logging
from typing import Dict, List, Any, Optional
from django. utils import timezone
from services.llm.ollama_client import get_ollama_client, OllamaError
from services.llm.prompts import (
 RULE_COMPILATION_SYSTEM,
 RULE_COMPILATION_TEMPLATE,
 format_prompt
)
from . models import Rule
logger = logging.getLogger(__name__)
class RuleCompiler:
 """
 Compiles user-written natural language rules into structured JSON
 using local Llama 3.2 3B model via Ollama.
 """

 def __init__(self):
 self.client = get_ollama_client()

 def compile_rules(
 self,
 subject,
 user_rules_text: str
 ) -> Dict[str, Any]:
 """
 Compile user rules text into structured format.

 Args:
 subject: Subject model instance
 user_rules_text: Plain English rules from user

 Returns:
 Dict with 'rules', 'errors', 'warnings' keys
 """
 # Check if Ollama is available
 if not self. client.is_available():
 raise RuleCompilationError(
 "Ollama is not running. Start it with: ollama serve"
 )

 # Prepare module names
 module_names = [
 subject.get_module_name(i)
 for i in range(1, subject.num_modules + 1)
 ]

 # Format prompt
 prompt = format_prompt(
 RULE_COMPILATION_TEMPLATE,
 subject_name=subject.name,
 num_modules=subject.num_modules,
 module_names=", ".join(module_names),
 user_rules=user_rules_text
 )

 try:
 # Call LLM
 result = self.client. generate_json(
 prompt=prompt,
 system=RULE_COMPILATION_SYSTEM
 )

 # Validate result structure
 if 'rules' not in result:
 result['rules'] = []
 if 'errors' not in result:
 result['errors'] = []
 if 'warnings' not in result:
 result['warnings'] = []

 # Validate each rule
 validated_rules = []
 for rule in result['rules']:
 validated = self._validate_rule(rule, subject. num_modules)
 if validated:
 validated_rules.append(validated)
 else:
 result['errors'].append(
 f"Invalid rule: {rule. get('original_text', 'Unknown')}"
 )

 result['rules'] = validated_rules
 return result

 except OllamaError as e:
 logger.error(f"Rule compilation failed: {e}")
 raise RuleCompilationError(str(e))

 def _validate_rule(
 self,
 rule: Dict[str, Any],
 num_modules: int
 ) -> Optional[Dict[str, Any]]:
 """Validate and clean a parsed rule."""

 # Required fields
 if 'action' not in rule or 'module' not in rule. get('action', {}):
 return None

 module = rule['action']['module']

 # Validate module number
 if not isinstance(module, int) or module < 1 or module > num_modules:
 return None

 # Ensure conditions exist
 if 'conditions' not in rule:
 rule['conditions'] = {}

 # Clean conditions
 conditions = rule['conditions']

 # Validate question_numbers
 if conditions.get('question_numbers'):
 conditions['question_numbers'] = [
 int(n) for n in conditions['question_numbers']
 if isinstance(n, (int, float)) and n > 0
 ]

 # Validate question_ranges
 if conditions.get('question_ranges'):
 valid_ranges = []
 for r in conditions['question_ranges']:
 if isinstance(r, list) and len(r) == 2:
 try:
 valid_ranges.append([int(r[0]), int(r[1])])
 except (ValueError, TypeError):
 pass
 conditions['question_ranges'] = valid_ranges

 # Ensure keywords are lowercase strings
 if conditions.get('keywords'):
 conditions['keywords'] = [
 str(k).lower(). strip()
 for k in conditions['keywords']
 if k
 ]

 # Generate ID if missing
 if not rule.get('id'):
 rule['id'] = f"rule_{hash(rule. get('original_text', ''))}"[:20]

 # Set default priority
 if 'priority' not in rule:
 rule['priority'] = 100

 return rule

 def save_compiled_rules(
 self,
 subject,
 compiled_result: Dict[str, Any],
 user,
 original_text: str
 ) -> List[Rule]:
 """
 Save compiled rules to database.

 Returns list of created Rule objects.
 """
 created_rules = []

 for i, rule_data in enumerate(compiled_result. get('rules', [])):
 rule = Rule. objects.create(
 subject=subject,
 name=rule_data. get('name', f'Rule {i + 1}'),
 description=rule_data. get('description', ''),
 rule_text=rule_data.get('original_text', ''),
 parsed_rule=rule_data,
 priority=rule_data. get('priority', 100),
 is_enabled=True,
 code_validated=True,
 created_by=user
 )
 created_rules.append(rule)

 return created_rules
class RuleCompilationError(Exception):
 """Raised when rule compilation fails."""
 pass
# Singleton instance
_compiler = None
def get_rule_compiler() -> RuleCompiler:
 """Get singleton RuleCompiler instance."""
 global _compiler
 if _compiler is None:
 _compiler = RuleCompiler()
 return _compiler
```
### Rule Executor Service
```python
# apps/rules/executor. py
import re
import logging
from typing import Optional, List, Dict, Any
from . models import Rule
logger = logging.getLogger(__name__)
class RuleExecutor:
 """
 Safely executes compiled classification rules against questions.
 Uses the parsed JSON rules directly without executing generated code.
 """

 def execute_rules(
 self,
 question,
 rules: List[Rule]
 ) -> Optional[Dict[str, Any]]:
 """
 Execute rules against a question and return match result.

 Args:
 question: Question model instance
 rules: List of Rule objects to execute (ordered by priority)

 Returns:
 Dict with 'module', 'rule_