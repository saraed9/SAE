from datetime import date
from main import app, db
from models.spectacle import GrandSpectacle, Spectacle

with app.app_context():
    db.create_all()

    if GrandSpectacle.query.first() is None:

        # =========================================================================
        # SPECTACLE 1 : Le Roi Lion
        # =========================================================================
        roi_lion = GrandSpectacle(
            nom="Le Roi Lion - La Comédie Musicale",
            description=(
                "Le spectacle musical culte revient dans une nouvelle mise en scène "
                "grandiose au Théâtre Mogador. Entre costumes impressionnants, "
                "chorégraphies spectaculaires et musiques mythiques d'Elton John, "
                "redécouvrez l'histoire de Simba dans une aventure immersive au cœur "
                "de la savane africaine."
            ),
            image="https://images.unsplash.com/photo-1546182990-dffeafbe841d?auto=format&fit=crop&w=800&q=80"
        )
        db.session.add(roi_lion)
        db.session.commit()

        db.session.add_all([
            Spectacle(
                grand_spectacle_id=roi_lion.id,
                titre="Le Roi Lion - La Comédie Musicale",
                date=date(2026, 10, 12),
                lieu="Théâtre Mogador, Paris",
                prix=69.00
            ),
            Spectacle(
                grand_spectacle_id=roi_lion.id,
                titre="Le Roi Lion - La Comédie Musicale",
                date=date(2026, 10, 13),
                lieu="Théâtre Mogador, Paris",
                prix=49.00
            ),
            Spectacle(
                grand_spectacle_id=roi_lion.id,
                titre="Le Roi Lion - La Comédie Musicale",
                date=date(2026, 10, 17),
                lieu="Théâtre Mogador, Paris",
                prix=59.00
            )
        ])

        # =========================================================================
        # SPECTACLE 2 : Bruno Mars
        # =========================================================================
        bruno_mars = GrandSpectacle(
            nom="Bruno Mars - The Romantic Tour",
            description=(
                "Bruno Mars revient avec The Romantic Tour, un spectacle inspiré des sonorités "
                "soul, funk et latines de son nouvel album. Entre lumières rétro, ambiance "
                "70s élégante, performances live des Hooligans et scénographie cinématographique, "
                "le show plonge le public dans un univers romantique et festif porté par "
                "des grooves vintage et ses plus grands tubes."
            ),
            image="https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80"
        )
        db.session.add(bruno_mars)
        db.session.commit()

        db.session.add_all([
            Spectacle(
                grand_spectacle_id=bruno_mars.id,
                titre="Bruno Mars - The Romantic Tour",
                date=date(2026, 7, 5),
                lieu="Stade de France, Saint-Denis",
                prix=89.00
            ),
            Spectacle(
                grand_spectacle_id=bruno_mars.id,
                titre="Bruno Mars - The Romantic Tour",
                date=date(2026, 7, 8),
                lieu="Groupama Stadium, Lyon",
                prix=79.00
            )
        ])

        # =========================================================================
        # SPECTACLE 3 : Casse-Noisette
        # =========================================================================
        casse_noisette = GrandSpectacle(
            nom="Casse-Noisette - Ballet Impérial",
            description=(
                "Le célèbre ballet de Tchaïkovski revient dans une version féerique "
                "portée par le Ballet National. Entre décors enneigés, costumes "
                "somptueux et musique intemporelle, laissez-vous emporter dans la "
                "magie des fêtes de fin d'année."
            ),
            image="https://images.unsplash.com/photo-1518834107812-67b0b7c58434?auto=format&fit=crop&w=800&q=80"
        )
        db.session.add(casse_noisette)
        db.session.commit()

        db.session.add_all([
            Spectacle(
                grand_spectacle_id=casse_noisette.id,
                titre="Casse-Noisette - Ballet Impérial",
                date=date(2026, 12, 23),
                lieu="Opéra Garnier, Paris",
                prix=85.00
            ),
            Spectacle(
                grand_spectacle_id=casse_noisette.id,
                titre="Casse-Noisette - Ballet Impérial",
                date=date(2026, 12, 24),
                lieu="Opéra Garnier, Paris",
                prix=110.00
            )
        ])

        # =========================================================================
        # SPECTACLE 4 : Festival Summer Peak
        # =========================================================================
        summer_fest = GrandSpectacle(
            nom="Summer Peak Festival",
            description=(
                "Trois jours de concerts en plein air réunissant les plus grandes "
                "têtes d'affiche pop, rock et électro. Entre scènes géantes, foodtrucks, "
                "animations nocturnes et camping immersif, Summer Peak promet une "
                "expérience estivale unique."
            ),
            image="https://images.unsplash.com/photo-1459749411175-04bf5292ceea?auto=format&fit=crop&w=800&q=80"
        )
        db.session.add(summer_fest)
        db.session.commit()

        db.session.add_all([
            Spectacle(
                grand_spectacle_id=summer_fest.id,
                titre="Summer Peak Festival",
                date=date(2026, 8, 21),
                lieu="Domaine National de Saint-Cloud, Paris",
                prix=65.00
            ),
            Spectacle(
                grand_spectacle_id=summer_fest.id,
                titre="Summer Peak Festival",
                date=date(2026, 8, 22),
                lieu="Domaine National de Saint-Cloud, Paris",
                prix=65.00
            ),
            Spectacle(
                grand_spectacle_id=summer_fest.id,
                titre="Summer Peak Festival",
                date=date(2026, 8, 21),
                lieu="Domaine National de Saint-Cloud, Paris",
                prix=159.00
            )
        ])

        # =========================================================================
        # SPECTACLE 5 : Le Lac des Cygnes
        # =========================================================================
        lac_cygnes = GrandSpectacle(
            nom="Le Lac des Cygnes sur Glace",
            description=(
                "Une adaptation spectaculaire du ballet mythique mêlant patinage "
                "artistique et danse classique. Entre effets lumineux, costumes élégants "
                "et performances acrobatiques, ce spectacle transporte le public dans "
                "un univers féerique et poétique."
            ),
            image="https://images.unsplash.com/photo-1518834107812-67b0b7c58434?auto=format&fit=crop&w=800&q=80"
        )
        db.session.add(lac_cygnes)
        db.session.commit()

        db.session.add_all([
            Spectacle(
                grand_spectacle_id=lac_cygnes.id,
                titre="Le Lac des Cygnes sur Glace",
                date=date(2026, 11, 14),
                lieu="Accor Arena, Paris",
                prix=49.00
            ),
            Spectacle(
                grand_spectacle_id=lac_cygnes.id,
                titre="Le Lac des Cygnes sur Glace",
                date=date(2026, 11, 15),
                lieu="Accor Arena, Paris",
                prix=39.00
            )
        ])

        # =========================================================================
        # SPECTACLE 6 : Hans Zimmer
        # =========================================================================
        hans_zimmer = GrandSpectacle(
            nom="Hans Zimmer Live Experience",
            description=(
                "Le compositeur légendaire aux multiples récompenses débarque avec un "
                "orchestre symphonique monumental pour revisiter les musiques cultes "
                "de Gladiator, Interstellar, Inception et Dune dans une expérience "
                "visuelle et sonore grandiose."
            ),
            image="https://images.unsplash.com/photo-1465847899084-d164df4dedc6?auto=format&fit=crop&w=800&q=80"
        )
        db.session.add(hans_zimmer)
        db.session.commit()

        db.session.add_all([
            Spectacle(
                grand_spectacle_id=hans_zimmer.id,
                titre="Hans Zimmer Live Experience",
                date=date(2026, 9, 18),
                lieu="Accor Arena, Paris",
                prix=95.00
            ),
            Spectacle(
                grand_spectacle_id=hans_zimmer.id,
                titre="Hans Zimmer Live Experience",
                date=date(2026, 9, 21),
                lieu="LDLC Arena, Lyon",
                prix=89.00
            )
        ])

        # =========================================================================
        # SPECTACLE 7 : Festival Electro
        # =========================================================================
        electro_night = GrandSpectacle(
            nom="Neon Pulse Festival",
            description=(
                "Le grand rendez-vous électro de l'été réunit DJs internationaux, "
                "shows lasers et scénographie futuriste dans une ambiance nocturne "
                "survoltée jusqu'au lever du soleil."
            ),
            image="https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=800&q=80"
        )
        db.session.add(electro_night)
        db.session.commit()

        db.session.add_all([
            Spectacle(
                grand_spectacle_id=electro_night.id,
                titre="Neon Pulse Festival",
                date=date(2026, 7, 17),
                lieu="Parc des Expositions, Lille",
                prix=59.00
            ),
            Spectacle(
                grand_spectacle_id=electro_night.id,
                titre="Neon Pulse Festival",
                date=date(2026, 7, 18),
                lieu="Parc des Expositions, Lille",
                prix=65.00
            )
        ])

        # =========================================================================
        # SPECTACLE 9 : Cirque Moderne
        # =========================================================================
        cirque_modern = GrandSpectacle(
            nom="Éclipse - Le Nouveau Cirque",
            description=(
                "Entre acrobaties aériennes, musique live et effets visuels immersifs, "
                "Éclipse réinvente le cirque contemporain dans une aventure poétique "
                "et spectaculaire inspirée des univers futuristes."
            ),
            image="https://images.unsplash.com/photo-1678270852355-7f2bbbe8811e?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        )
        db.session.add(cirque_modern)
        db.session.commit()

        db.session.add_all([
            Spectacle(
                grand_spectacle_id=cirque_modern.id,
                titre="Éclipse - Le Nouveau Cirque",
                date=date(2026, 10, 2),
                lieu="Zénith de Strasbourg",
                prix=54.00
            ),
            Spectacle(
                grand_spectacle_id=cirque_modern.id,
                titre="Éclipse - Le Nouveau Cirque",
                date=date(2026, 10, 4),
                lieu="Zénith de Strasbourg",
                prix=49.00
            )
        ])

        # =========================================================================
        # SPECTACLE 10 : Jazz
        # =========================================================================
        jazz_night = GrandSpectacle(
            nom="Blue Note Legends",
            description=(
                "Une soirée jazz élégante réunissant les plus grands musiciens de la "
                "scène contemporaine. Entre improvisations, ambiance feutrée et grands "
                "classiques revisités, Blue Note Legends promet une immersion musicale "
                "authentique."
            ),
            image="https://images.unsplash.com/photo-1511192336575-5a79af67a629?auto=format&fit=crop&w=800&q=80"
        )
        db.session.add(jazz_night)
        db.session.commit()

        db.session.add_all([
            Spectacle(
                grand_spectacle_id=jazz_night.id,
                titre="Blue Note Legends",
                date=date(2026, 6, 14),
                lieu="L'Olympia, Paris",
                prix=48.00
            ),
            Spectacle(
                grand_spectacle_id=jazz_night.id,
                titre="Blue Note Legends",
                date=date(2026, 6, 15),
                lieu="L'Olympia, Paris",
                prix=52.00
            )
        ])

        # =========================================================================
        # SPECTACLE 11 : Spectacle Médiéval
        # =========================================================================
        medieval_show = GrandSpectacle(
            nom="Les Flammes du Royaume",
            description=(
                "Chevaliers, combats épiques, cascades à cheval et effets pyrotechniques "
                "plongent les spectateurs dans une fresque médiévale spectaculaire inspirée "
                "des univers fantastiques."
            ),
            image="https://images.unsplash.com/photo-1519677100203-a0e668c92439?auto=format&fit=crop&w=800&q=80"
        )
        db.session.add(medieval_show)
        db.session.commit()

        db.session.add_all([
            Spectacle(
                grand_spectacle_id=medieval_show.id,
                titre="Les Flammes du Royaume",
                date=date(2026, 8, 7),
                lieu="Arènes de Nîmes",
                prix=42.00
            ),
            Spectacle(
                grand_spectacle_id=medieval_show.id,
                titre="Les Flammes du Royaume",
                date=date(2026, 8, 8),
                lieu="Arènes de Nîmes",
                prix=45.00
            )
        ])

        # =========================================================================
        # SPECTACLE 12 : K-pop
        # =========================================================================
        kpop_show = GrandSpectacle(
            nom="Seoul Lights World Tour",
            description=(
                "Le phénomène mondial de la K-pop débarque en France avec un show "
                "spectaculaire mêlant chorégraphies millimétrées, écrans géants, "
                "effets visuels futuristes et performances explosives."
            ),
            image="https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=800&q=80"
        )
        db.session.add(kpop_show)
        db.session.commit()

        db.session.add_all([
            Spectacle(
                grand_spectacle_id=kpop_show.id,
                titre="Seoul Lights World Tour",
                date=date(2026, 5, 30),
                lieu="Paris La Défense Arena",
                prix=99.00
            ),
            Spectacle(
                grand_spectacle_id=kpop_show.id,
                titre="Seoul Lights World Tour",
                date=date(2026, 6, 2),
                lieu="Le Dôme, Marseille",
                prix=85.00
            )
        ])

        # =========================================================================
        # SAUVEGARDE FINALE
        # =========================================================================
        db.session.commit()