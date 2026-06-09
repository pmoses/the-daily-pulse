"""
Management command to seed the database with demo news content.
Run once after migrations to get a working demo site.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from wagtail.models import Page, Site


CATEGORIES = [
    {"name": "World", "slug": "world", "color": "blue"},
    {"name": "Technology", "slug": "technology", "color": "indigo"},
    {"name": "Business", "slug": "business", "color": "emerald"},
    {"name": "Science", "slug": "science", "color": "cyan"},
    {"name": "Politics", "slug": "politics", "color": "red"},
    {"name": "Sports", "slug": "sports", "color": "amber"},
    {"name": "Culture", "slug": "culture", "color": "purple"},
]

AUTHORS = [
    {"name": "Sarah Chen", "role": "Senior Correspondent", "bio": "Award-winning journalist covering global affairs and technology."},
    {"name": "Marcus Webb", "role": "Political Editor", "bio": "15 years covering domestic and international politics."},
    {"name": "Priya Nair", "role": "Science Reporter", "bio": "Former research scientist turned science communicator."},
    {"name": "James Okafor", "role": "Business Analyst", "bio": "Covers markets, economy, and corporate affairs."},
    {"name": "Elena Reyes", "role": "Culture & Arts", "bio": "Writes about film, music, literature and the arts."},
]

ARTICLES = [
    {
        "title": "Global Climate Summit Reaches Historic Agreement on Carbon Emissions",
        "summary": "World leaders gathered in Geneva have signed a landmark accord committing 140 nations to achieve net-zero carbon emissions by 2045, a decade earlier than previous targets.",
        "body": "<p>In what diplomats are calling the most significant climate deal since Paris, representatives from 140 nations signed the Geneva Accord late Tuesday after three days of intensive negotiations.</p><p>The agreement commits signatories to reaching net-zero carbon emissions by 2045, a decade earlier than the targets set in previous international frameworks. Crucially, it includes binding enforcement mechanisms and a $500 billion climate adaptation fund for developing nations.</p><p>\"This is the moment history demanded of us,\" said UN Secretary-General António Guterres. \"We have moved from promises to action.\"</p><p>Economists estimate the transition will require restructuring energy systems, transportation networks, and industrial processes across every participating economy — but say the cost of inaction would be far greater.</p>",
        "category": "world",
        "author": "Sarah Chen",
        "reading_time": 4,
        "featured": True,
        "breaking": False,
    },
    {
        "title": "OpenAI Unveils Model That Can Reason About Physical World",
        "summary": "The new AI system demonstrates unprecedented ability to understand spatial relationships and predict real-world outcomes, raising both excitement and concern.",
        "body": "<p>OpenAI on Wednesday released a preview of its latest artificial intelligence model, one the company says can reason about the physical world with a degree of accuracy that far surpasses previous systems.</p><p>The model, called Orion-3, can analyze video footage and predict how objects will move, understand complex spatial relationships, and generate accurate physical simulations — capabilities that have long eluded AI researchers.</p><p>Demonstrations showed the system correctly predicting the outcome of physics experiments it had never seen, diagnosing structural weaknesses in architectural plans, and planning robotic movements with precision comparable to specialized industrial systems.</p><p>The announcement has sparked immediate debate among AI safety researchers, some of whom warn that systems capable of reasoning about physical systems could be misused.</p>",
        "category": "technology",
        "author": "Priya Nair",
        "reading_time": 5,
        "featured": False,
        "breaking": True,
    },
    {
        "title": "Federal Reserve Signals Shift in Interest Rate Policy",
        "summary": "Fed Chair signals a more cautious approach to rate cuts as inflation data sends mixed signals to policymakers.",
        "body": "<p>Federal Reserve Chair Jerome Powell struck a notably cautious tone at Wednesday's press conference following the central bank's decision to hold interest rates steady, suggesting the path to rate cuts may be longer and more uncertain than markets had anticipated.</p><p>\"The data has been mixed,\" Powell said, citing persistent services inflation alongside cooling goods prices. \"We need greater confidence that inflation is moving sustainably toward our 2 percent goal before we begin to ease policy.\"</p><p>Markets reacted sharply, with the S&amp;P 500 falling 1.4% and Treasury yields rising as investors repriced their expectations for the timing and magnitude of rate cuts this year.</p>",
        "category": "business",
        "author": "James Okafor",
        "reading_time": 3,
        "featured": False,
        "breaking": False,
    },
    {
        "title": "Scientists Detect Unusual Radio Signals From Nearby Star System",
        "summary": "Astronomers at the Parkes Observatory have recorded a series of structured radio emissions from Proxima Centauri b that defy conventional astrophysical explanations.",
        "body": "<p>Researchers at the Parkes Observatory in Australia have detected a series of unusual radio signals originating from the direction of Proxima Centauri, the nearest star system to Earth, located just 4.2 light-years away.</p><p>The signals, recorded over six observation windows spanning three months, display a regularity and narrow bandwidth that distinguish them from known natural phenomena such as pulsars or magnetars.</p><p>\"We've ruled out the most obvious sources of interference,\" said Dr. Amara Singh, lead author of the paper submitted to Nature Astronomy. \"What we're left with is genuinely puzzling.\"</p><p>The team is careful to avoid any suggestion of an extraterrestrial intelligence, noting that instrumental artifacts or previously uncharacterized astrophysical processes remain the most likely explanations. Additional observations are planned using the Square Kilometre Array.</p>",
        "category": "science",
        "author": "Priya Nair",
        "reading_time": 6,
        "featured": False,
        "breaking": True,
    },
    {
        "title": "Senate Passes Landmark Infrastructure and Housing Reform Bill",
        "summary": "The bipartisan Infrastructure and Housing Act passed 67-33, authorizing $1.2 trillion for roads, transit, broadband, and affordable housing construction.",
        "body": "<p>The Senate voted 67-33 Thursday to pass the Infrastructure and Housing Modernization Act, a sweeping $1.2 trillion package that would fund roads, bridges, mass transit, broadband expansion, and the largest affordable housing construction program in decades.</p><p>The bill now heads to the House, where leaders have signaled strong support for passage before the August recess.</p><p>\"This is generational investment in the foundations of American life,\" said Senate Majority Leader Chuck Schumer. \"It is rare that the Senate speaks with this degree of bipartisan clarity.\"</p><p>The housing component — $280 billion over ten years — represents the largest federal commitment to affordable housing since the New Deal era, according to the National Low Income Housing Coalition.</p>",
        "category": "politics",
        "author": "Marcus Webb",
        "reading_time": 4,
        "featured": False,
        "breaking": False,
    },
    {
        "title": "Cannes Palme d'Or Goes to Iranian Director's Debut Feature",
        "summary": "Leila Mohammadi's debut film \"The Orchard\" wins Cannes' highest honor in a surprise decision that drew a standing ovation from the jury and audience alike.",
        "body": "<p>Leila Mohammadi's debut feature film, \"The Orchard,\" was awarded the Palme d'Or at the 77th Cannes Film Festival in a decision that surprised many industry watchers who had expected the prize to go to one of several more established contenders.</p><p>The film, a sparse and devastating portrayal of three generations of women in rural Iran, was shot over two years on a minimal budget using a cast of nonprofessional actors.</p><p>\"I made this film for my mother, my grandmother, and all the women whose stories are never told,\" Mohammadi said through tears in her acceptance speech, which was met with a prolonged standing ovation.</p><p>The jury, chaired by Greta Gerwig, praised the film's restraint and emotional honesty as \"a reminder of what cinema can do that no other art form can.\"</p>",
        "category": "culture",
        "author": "Elena Reyes",
        "reading_time": 4,
        "featured": False,
        "breaking": False,
    },
    {
        "title": "Tech Giants Face New EU Antitrust Probe Over AI Market Practices",
        "summary": "European Commission opens investigations into whether major AI companies are using market dominance in cloud computing to unfairly advantage their AI products.",
        "body": "<p>The European Commission announced Thursday it is opening formal antitrust investigations into three major technology companies over concerns that their dominance in cloud computing infrastructure is being leveraged to give their artificial intelligence products an unfair advantage.</p><p>The probe, which targets practices related to API pricing, data access, and technical interoperability, comes just months after the EU's AI Act entered into force.</p><p>\"Competition in artificial intelligence markets is not a given — it must be actively protected,\" said EU Competition Commissioner Teresa Ribera. \"We will not allow the mistakes of the social media era to be repeated.\"</p><p>The companies under investigation have 30 days to respond to the Commission's preliminary findings.</p>",
        "category": "technology",
        "author": "James Okafor",
        "reading_time": 3,
        "featured": False,
        "breaking": False,
    },
    {
        "title": "World Cup 2026 Host Cities Reveal Upgraded Stadium Plans",
        "summary": "Sixteen host cities across the US, Canada, and Mexico unveiled their final stadium configurations, with capacity upgrades promising record attendance figures.",
        "body": "<p>The sixteen host cities for the 2026 FIFA World Cup unveiled their final stadium and infrastructure plans this week, with several cities announcing last-minute capacity expansions that could see the tournament set new attendance records.</p><p>Dallas's AT&amp;T Stadium will be reconfigured to hold 110,000 fans for the final — the largest stadium capacity in World Cup history. New York/New Jersey's MetLife Stadium will host eight matches, including both semifinals.</p><p>FIFA president Gianni Infantino called the preparations \"unprecedented in the history of the sport,\" while acknowledging that ticket prices have drawn criticism from fan groups who argue the event is increasingly inaccessible to ordinary supporters.</p>",
        "category": "sports",
        "author": "Marcus Webb",
        "reading_time": 3,
        "featured": False,
        "breaking": False,
    },
    {
        "title": "New Research Links Ultra-Processed Foods to Accelerated Aging",
        "summary": "A longitudinal study of 45,000 adults finds a strong association between ultra-processed food consumption and biological aging markers — an alarming finding for public health.",
        "body": "<p>A major new study published in the journal Cell Metabolism has found a strong association between high consumption of ultra-processed foods and accelerated biological aging, as measured by DNA methylation markers that predict age-related disease risk.</p><p>The research, which followed 45,000 adults in ten countries over twelve years, found that individuals in the highest quartile of ultra-processed food consumption showed biological aging markers roughly 2.4 years ahead of their chronological age compared with those in the lowest quartile.</p><p>\"This adds to a growing body of evidence that what we eat affects not just our weight or cardiovascular risk, but the fundamental aging processes at the cellular level,\" said Dr. Carlos Mendes, a co-author of the study at the University of São Paulo.</p>",
        "category": "science",
        "author": "Priya Nair",
        "reading_time": 5,
        "featured": False,
        "breaking": False,
    },
]


class Command(BaseCommand):
    help = "Seed the database with demo news content"

    def add_arguments(self, parser):
        parser.add_argument("--no-input", action="store_true", help="Skip confirmation prompt")

    def handle(self, *args, **options):
        from news.models import NewsArticlePage, NewsAuthor, NewsCategory, NewsIndexPage

        if NewsIndexPage.objects.exists():
            self.stdout.write(self.style.WARNING("News content already seeded — skipping"))
            return

        self.stdout.write("Seeding categories...")
        cat_map = {}
        for cat_data in CATEGORIES:
            cat, _ = NewsCategory.objects.get_or_create(
                slug=cat_data["slug"],
                defaults={"name": cat_data["name"], "color": cat_data["color"]},
            )
            cat_map[cat_data["slug"]] = cat

        self.stdout.write("Seeding authors...")
        author_map = {}
        for author_data in AUTHORS:
            author, _ = NewsAuthor.objects.get_or_create(
                name=author_data["name"],
                defaults={"role": author_data["role"], "bio": author_data["bio"]},
            )
            author_map[author_data["name"]] = author

        self.stdout.write("Creating index page...")
        root = Page.objects.filter(depth=1).first()
        if not root:
            self.stdout.write(self.style.ERROR("Root page not found — run migrations first"))
            return

        # Remove default welcome page so we can take its place
        existing_children = root.get_children()
        for child in existing_children:
            if child.slug in ("home", "welcome-to-your-new-wagtail-site"):
                child.delete()

        index_page = NewsIndexPage(
            title="The Daily Pulse",
            slug="daily-pulse",
            tagline="Breaking news, in-depth stories, and investigative journalism",
        )
        root.add_child(instance=index_page)

        # Update the default site to point to this page
        try:
            site = Site.objects.get(is_default_site=True)
            site.root_page = index_page
            site.hostname = "localhost"
            site.port = 8000
            site.save()
        except Site.DoesNotExist:
            Site.objects.create(
                hostname="localhost",
                port=8000,
                root_page=index_page,
                is_default_site=True,
                site_name="The Daily Pulse",
            )

        self.stdout.write("Creating articles...")
        for i, article_data in enumerate(ARTICLES):
            author = author_map.get(article_data["author"])
            category = cat_map.get(article_data["category"])

            article = NewsArticlePage(
                title=article_data["title"],
                slug=f"article-{i + 1}",
                summary=article_data["summary"],
                body=article_data["body"],
                author=author,
                reading_time=article_data["reading_time"],
                featured=article_data.get("featured", False),
                breaking=article_data.get("breaking", False),
                first_published_at=timezone.now(),
            )
            index_page.add_child(instance=article)
            if category:
                article.categories.add(category)
                article.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(ARTICLES)} articles across {len(CATEGORIES)} categories"))
