# Medical Education System - Documentation

## Overview

The Medical Education System provides comprehensive, layered, personalized medical information for the Briz-L Eye Clinic chatbot. It delivers intelligent educational content adapted to each patient's knowledge level, emotional state, and language preference.

## Features

### 🎯 Core Capabilities

- **Progressive Disclosure**: Information revealed layer by layer, starting simple and getting more detailed
- **Multi-Language Support**: Full content in Azerbaijani (az), Russian (ru), and English (en)
- **Personalization**: Content adapted based on:
  - Patient's knowledge level (lay, intermediate, advanced)
  - Emotional state (anxious, neutral, confident)
  - Urgency level
  - Conversation history
- **Semantic Search**: Intelligent content discovery with synonym matching
- **FAQ Database**: Comprehensive frequently asked questions

### 📚 Content Coverage

**Conditions:**
- Cataract (Katarakta)
- More conditions can be added following the same template

**Procedures:**
- Excimer Laser (LASIK/PRK/SMILE)
- More procedures can be added following the same template

**FAQs:**
- General eye health questions
- Surgery-specific questions
- Pricing information (can be expanded)

## Architecture

```
medical_education/
├── content/              # YAML content files
│   ├── conditions/       # Eye conditions database
│   ├── procedures/       # Procedure descriptions
│   ├── prevention/       # Prevention guides
│   └── postop/          # Post-operative care
├── faqs/                # FAQ database
├── core/                # Python modules
│   ├── content_retriever.py
│   ├── progressive_disclosure.py
│   ├── personalization_engine.py
│   └── semantic_search.py
├── actions/             # Rasa actions
│   └── action_educate.py
└── tests/               # Unit tests
```

## Usage

### In Rasa Conversations

**Example 1: Asking about a condition**
```
User: Katarakta nədir?
Bot: [Simple explanation layer]
     Katarakta göz lensinin dumanlı olmasıdır...
     
User: Daha ətraflı
Bot: [Symptoms layer]
     ƏLAMƏTLƏR:
     Early stage: Yüngül dumanlı görmə...
```

**Example 2: Asking about a procedure**
```
User: LASIK əməliyyatı haqqında
Bot: [Simple explanation]
     Lazer göz əməliyyatı gözlükdən azad olmaq üçündür...
```

**Example 3: Searching**
```
User: göz əməliyyatları
Bot: [Search results]
     1. Katarakta (Xəstəlik)
     2. Excimer Lazer (Prosedur)
```

### Progressive Disclosure Layers

Information is revealed in this sequence:
1. **simple_explanation** - Basic, patient-friendly explanation
2. **symptoms** - What to look for
3. **medical_details** - More technical information
4. **treatment** - Treatment options
5. **risks** - Risks and complications
6. **recovery** - Recovery timeline
7. **cost** - Pricing information
8. **faqs** - Frequently asked questions

### Personalization Examples

**For Anxious Patients:**
```yaml
# System detects fear keywords: "qorxuram", "təhlükəli"
# Adds reassurance:
💙 Narahat olmayın! Bu prosedur çox təhlükəsizdir...
```

**For Lay Audience:**
```yaml
# Simplifies medical jargon:
"fakoemulsifikasiya (ultrasəs ilə lens əridilməsi)"
```

**For Emergency Cases:**
```yaml
# Prioritizes urgent information:
🚨 DİQQƏT: Təcili simptomlar olduğu təqdirdə...
```

## Integration with Existing Systems

### Language Detection
Uses existing `detected_language` slot from your multi-language system.

### Triage System
Can be triggered after triage to provide relevant educational content.

### Example Integration:
```yaml
# After triage identifies cataract symptoms
- action: action_triage_patient
- action: action_educate  # Auto-provides cataract info
```

## Adding New Content

### Creating a New Condition

1. Create `medical_education/content/conditions/your_condition.yml`
2. Follow the structure in `cataract.yml`:
   - Define condition metadata (id, name, alternate_names)
   - Add all 12 layers of information
   - Provide content in all 3 languages

### Creating a New Procedure

1. Create `medical_education/content/procedures/your_procedure.yml`
2. Follow the structure in `excimer_laser.yml`
3. Include candidacy criteria, procedure types, timeline, etc.

### Adding FAQs

Add entries to:
- `faqs/general_faqs.yml` - General questions
- `faqs/surgery_faqs.yml` - Surgery-specific
- `faqs/pricing_faqs.yml` - Cost-related

## Testing

### Run Unit Tests
```bash
cd medical_education
pytest tests/test_medical_education.py -v
```

### Test Coverage
- Content retrieval and caching
- Layer-based access
- Progressive disclosure logic
- Personalization engine
- Semantic search
- FAQ matching

### Manual Testing
```bash
# Train Rasa model
rasa train

# Test in shell
rasa shell

# Try these:
User: katarakta nədir
User: daha ətraflı
User: LASIK haqqında
User: qiymət nə qədərdir
```

## API Reference

### MedicalContentRetriever

```python
from medical_education.core.content_retriever import MedicalContentRetriever

retriever = MedicalContentRetriever()

# Get condition
cataract = retriever.get_condition('cataract', language='az')

# Get specific layer
simple = retriever.get_layer('condition', 'cataract', 'simple_explanation', 'az')

# Search FAQs
faqs = retriever.search_faqs('ağrı', 'az')

# Find by name
result = retriever.find_content_by_name('katarakta', 'az')
```

### ProgressiveDisclosure

```python
from medical_education.core.progressive_disclosure import ProgressiveDisclosure

progressive = ProgressiveDisclosure()

# Get next layer
layer_data = progressive.get_next_layer('condition', 'cataract', depth=0, language='az')

# Format for chat
message = progressive.format_for_chat(layer_data, 'az')

# Get summary
summary = progressive.get_summary('condition', 'cataract', 'az')
```

### PersonalizationEngine

```python
from medical_education.core.personalization_engine import PersonalizationEngine

personalizer = PersonalizationEngine()

# Detect knowledge level
level = personalizer.detect_knowledge_level(user_messages)

# Detect emotional state
state = personalizer.detect_emotional_state(message, 'az')

# Personalize content
personalized = personalizer.personalize_content(
    content,
    knowledge_level='lay',
    emotional_state='anxious',
    language='az'
)
```

### SemanticSearch

```python
from medical_education.core.semantic_search import SemanticSearch

search = SemanticSearch()

# Search
results = search.search('katarakta', 'az', limit=5)

# Suggest queries
suggestions = search.suggest_queries('kata', 'az', limit=5)
```

## Configuration

### Slots in domain.yml
- `education_topic` - Current topic (e.g., "cataract")
- `education_type` - Type: "condition" or "procedure"
- `education_depth` - Current layer depth (0-7)
- `education_layer` - Current layer name
- `detected_language` - User's language

### Intents
- `ask_about_condition` - Questions about medical conditions
- `ask_about_procedure` - Questions about procedures
- `ask_more_details` - Request for more information
- `ask_faq` - FAQ queries
- `search_medical_info` - General search
- `list_conditions` - List available content

## Maintenance

### Updating Existing Content
1. Edit the relevant YAML file
2. Content is automatically reloaded on next Rasa restart
3. No code changes needed

### Adding Languages
1. Add language code to all YAML files
2. Update synonym dictionaries in `semantic_search.py`
3. Update prompts in `progressive_disclosure.py`
4. Update reassurance messages in `personalization_engine.py`

## Performance

- **Content Caching**: All YAML files preloaded into memory
- **Fast Retrieval**: O(1) access to cached content
- **Search**: Linear scan with relevance scoring
- **Memory Usage**: ~1-2MB per language for full content set

## Future Enhancements

### Potential Additions
- [ ] Add more conditions (glaucoma, diabetic retinopathy, dry eye, AMD)
- [ ] Add more procedures (YAG laser, phacoemulsification details)
- [ ] Prevention guides
- [ ] Post-operative care instructions
- [ ] Patient testimonials with real experiences
- [ ] Video/diagram media integration
- [ ] Appointment booking integration after education
- [ ] Analytics on popular questions

### Advanced Features
- [ ] Machine learning-based search (embeddings)
- [ ] Adaptive layer sequencing based on user engagement
- [ ] Integration with medical knowledge graphs
- [ ] Voice output optimization
- [ ] Visual aids and diagrams

## Support

For questions or issues:
1. Check unit tests for usage examples
2. Review YAML templates in `cataract.yml` and `excimer_laser.yml`
3. Consult implementation plan in artifacts

## License

Part of Briz-L Eye Clinic chatbot system.
