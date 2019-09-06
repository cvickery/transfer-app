"""   Institutions that have academic programs registered with NYS Department of Education.
      Includes all known CUNY colleges plus other institutions that have M/I programs with a CUNY
      institution.
      For each institution, the institution id number (as a string), the institution name,
      as spelled on the NYS website, and a boolean to indicate whether it is a CUNY college or not.

      NOTE:THESE VALUES ARE NOT UPDATED AUTOMATICALLY
"""
known_institutions = {}
known_institutions['bar'] = ('33050', 'CUNY BARUCH COLLEGE', True)
known_institutions['bcc'] = ('37100', 'BRONX COMM COLL', True)
known_institutions['bkl'] = ('33100', 'CUNY BROOKLYN COLL', True)
known_institutions['bmc'] = ('37050', 'BOROUGH MANHATTAN COMM C', True)
known_institutions['cty'] = ('33150', 'CUNY CITY COLLEGE', True)
known_institutions['csi'] = ('33180', 'CUNY COLL STATEN ISLAND', True)
known_institutions['grd'] = ('31050', 'CUNY GRADUATE SCHOOL', True)
known_institutions['hos'] = ('37150', 'HOSTOS COMM COLL', True)
known_institutions['htr'] = ('33250', 'CUNY HUNTER COLLEGE', True)
known_institutions['jjc'] = ('33300', 'CUNY JOHN JAY COLLEGE', True)
known_institutions['kcc'] = ('37250', 'KINGSBOROUGH COMM COLL', True)
known_institutions['lag'] = ('37200', 'LA GUARDIA COMM COLL', True)
known_institutions['law'] = ('31100', 'CUNY LAW SCHOOL AT QUEENS', True)
known_institutions['leh'] = ('33200', 'CUNY LEHMAN COLLEGE', True)
known_institutions['mec'] = ('37280', 'MEDGAR EVERS COLL', True)
known_institutions['ncc'] = ('33350', 'STELLA & CHAS GUTTMAN CC', True)
known_institutions['nyt'] = ('33380', 'NYC COLLEGE OF TECHNOLOGY', True)
known_institutions['qcc'] = ('37350', 'QUEENSBOROUGH COMM COLL', True)
known_institutions['qns'] = ('33400', 'CUNY QUEENS COLLEGE', True)
known_institutions['sps'] = ('31051', 'CUNY SCHOOL OF PROF STUDY', True)
known_institutions['yrk'] = ('33500', 'CUNY YORK COLLEGE', True)
# known_institutions['bst'] = ('40450', 'BANK STREET COLLEGE OF ED', False)
# known_institutions['bls'] = ('40900', 'BROOKLYN LAW SCHOOL', False)
# known_institutions['uts'] = ('47350', 'UNION THEOLOGICAL SEM', False)
# known_institutions['nyl'] = ('45100', 'NEW YORK LAW SCHOOL', False)
# known_institutions['sco'] = ('24150', 'SUNY COL OF OPTOMETRY', False)

""" The following is a list of all NYS institutions,including the ones already listed above, using
    the institution ID as the index. Needed for CUNY programs that have variants at non-CUNY
    schools. But, also, using the institution ID, registered programs could look up the programs for
    these schools as well.
    List last updated on May 2, 2019
"""
known_institutions['402600'] = ('402600', 'ACAD FOR JEWISH RELIGION', False)
known_institutions['401000'] = ('401000', 'ADELPHI UNIVERSITY', False)
known_institutions['270300'] = ('270300', 'ADIRONDACK COMM COLL', False)
known_institutions['401500'] = ('401500', 'ALB COLL PHARM & HLTH SCI', False)
known_institutions['601000'] = ('601000', 'ALB-SCHO-SCHEN-SARA BOCES', False)
known_institutions['402000'] = ('402000', 'ALBANY LAW SCHOOL', False)
known_institutions['402500'] = ('402500', 'ALBANY MEDICAL COLLEGE', False)
known_institutions['402510'] = ('402510', 'ALBERT EINSTEIN COLLEGE', False)
known_institutions['403000'] = ('403000', 'ALFRED UNIVERSITY-MAIN', False)
known_institutions['403500'] = ('403500', 'AMER ACAD DRAMATIC ARTS', False)
known_institutions['403700'] = ('403700', 'AMER ACADEMY MCALLISTER', False)
known_institutions['601650'] = ('601650', 'AMER INST FOR PSYCHOANAL', False)
known_institutions['403800'] = ('403800', 'AMER MUSEUM NAT HISTORY', False)
known_institutions['601600'] = ('601600', 'AMERICAN COL ACUPUNCTURE', False)
known_institutions['602100'] = ('602100', 'AMERICAN INTER ACUP INST', False)
known_institutions['802089'] = ('802089', 'AMERICAN UNIV OF BEIRUT', False)
known_institutions['515000'] = ('515000', 'AMG SCHL LIC PRACT NURSNG', False)
known_institutions['602000'] = ('602000', 'ARNOT-OGDEN MED CTR SCH N', False)
known_institutions['508800'] = ('508800', 'ART INSTITUTE OF NYC', False)
known_institutions['500710'] = ('500710', 'ASA COLLEGE-MANHATTAN', False)
known_institutions['500700'] = ('500700', 'ASA COLLEGE, INC.', False)
known_institutions['404500'] = ('404500', 'BANK STREET COLLEGE OF ED', False)
known_institutions['800577'] = ('800577', 'BAR-ILAN UNIV', False)
known_institutions['405000'] = ('405000', 'BARD COLLEGE', False)
known_institutions['405010'] = ('405010', 'BARD GRADUATE CENTER', False)
known_institutions['405020'] = ('405020', 'BARD-BROOKLYN PUBLIC LIB.', False)
known_institutions['405500'] = ('405500', 'BARNARD COLLEGE', False)
known_institutions['502020'] = ('502020', 'BERKELEY C-WESTCHESTER C', False)
known_institutions['502000'] = ('502000', 'BERKELEY COLLEGE', False)
known_institutions['502030'] = ('502030', 'BERKELEY COLLEGE-BROOKLYN', False)
known_institutions['630100'] = ('630100', 'BLANTON-PEALE INSTITUTE', False)
known_institutions['407000'] = ('407000', 'BORICUA COLLEGE', False)
known_institutions['407020'] = ('407020', 'BORICUA COLLEGE-BRONX', False)
known_institutions['407010'] = ('407010', 'BORICUA COLLEGE/BROOKLYN', False)
known_institutions['370500'] = ('370500', 'BOROUGH MANHATTAN COMM C', False)
known_institutions['407500'] = ('407500', 'BRAMSON ORT COLLEGE', False)
known_institutions['502800'] = ('502800', 'BRIARCLIFFE COLLEGE', False)
known_institutions['502850'] = ('502850', 'BRIARCLIFFE COLLEGE-BOHEM', False)
known_institutions['371000'] = ('371000', 'BRONX COMM COLL', False)
known_institutions['602300'] = ('602300', 'BRONX-LEBANON HOSP CENTER', False)
known_institutions['602400'] = ('602400', 'BROOKLYN INST OF MASS TH', False)
known_institutions['409000'] = ('409000', 'BROOKLYN LAW SCHOOL', False)
known_institutions['270600'] = ('270600', 'BROOME COMM COLL', False)
known_institutions['602500'] = ('602500', 'BROOME-DELA-TIOGA BOCES', False)
known_institutions['501000'] = ('501000', 'BRYANT&STRAT C - ALBANY', False)
known_institutions['503010'] = ('503010', 'BRYANT&STRAT C - AMHERST', False)
known_institutions['503000'] = ('503000', 'BRYANT&STRAT C - BUFFALO', False)
known_institutions['503500'] = ('503500', 'BRYANT&STRAT C - GREECE', False)
known_institutions['509500'] = ('509500', 'BRYANT&STRAT C - SYRACUSE', False)
known_institutions['503510'] = ('503510', 'BRYANT&STRAT C -HENRIETTA', False)
known_institutions['503020'] = ('503020', 'BRYANT&STRAT C-SOUTHTOWNS', False)
known_institutions['509510'] = ('509510', 'BRYANT&STRAT C-SYR NORTH', False)
known_institutions['603000'] = ('603000', 'BUFFALO VOC/TECH CENTER', False)
known_institutions['410000'] = ('410000', 'CANISIUS COLLEGE', False)
known_institutions['605500'] = ('605500', 'CATT-ALLE-ERIE-WYOM BOCES', False)
known_institutions['270910'] = ('270910', 'CAYUGA CCC - FULTON', False)
known_institutions['270900'] = ('270900', 'CAYUGA COUNTY COMM COLL', False)
known_institutions['606000'] = ('606000', 'CAYUGA-ONONDAGA BOCES', False)
known_institutions['411500'] = ('411500', 'CAZENOVIA COLLEGE', False)
known_institutions['630120'] = ('630120', 'CENT FOR MOD PSYCHOAN STU', False)
known_institutions['630130'] = ('630130', 'CENTER FOR HUMAN DEVELOP', False)
known_institutions['800400'] = ('800400', 'CENTRAL EUR U-BUCHAREST', False)
known_institutions['803570'] = ('803570', 'CENTRAL EUR UNIV BUDA CAM', False)
known_institutions['800443'] = ('800443', 'CENTRAL EUR UNIV PRAG CAM', False)
known_institutions['800410'] = ('800410', 'CENTRAL EUROPEAN UNIV-NY', False)
known_institutions['809900'] = ('809900', 'CERGE-EI', False)
known_institutions['630600'] = ('630600', 'CG JUNG INSTITUTE OF NY', False)
known_institutions['412000'] = ('412000', 'CHRIST THE KING SEMINARY', False)
known_institutions['504300'] = ('504300', 'CHRISTIE\'S ED, INC', False)
known_institutions['412010'] = ('412010', 'CITY SEMINARY-NY GRAD CTR', False)
known_institutions['607000'] = ('607000', 'CLARA BARTON HS/HLTH PROF', False)
known_institutions['412510'] = ('412510', 'CLARKSON UNIV CAPITAL REG', False)
known_institutions['412500'] = ('412500', 'CLARKSON UNIVERSITY', False)
known_institutions['619500'] = ('619500', 'CLIN-ESSEX-WAR-WASH BOCES', False)
known_institutions['271200'] = ('271200', 'CLINTON COMM COLL', False)
known_institutions['412700'] = ('412700', 'COCHRAN SCHOOL NURSING', False)
known_institutions['415540'] = ('415540', 'COL NEW ROCH-NY THEOL SEM', False)
known_institutions['412900'] = ('412900', 'COLD SPRING HARBOR LAB', False)
known_institutions['413500'] = ('413500', 'COLGATE UNIVERSITY', False)
known_institutions['413000'] = ('413000', 'COLGATE-ROCH CROZER DIV S', False)
known_institutions['415530'] = ('415530', 'COLL NEW ROCH-JC O\'CONNOR', False)
known_institutions['415550'] = ('415550', 'COLL NEW ROCHELLE-BRKLYN', False)
known_institutions['415500'] = ('415500', 'COLL NEW ROCHELLE-MAIN', False)
known_institutions['415560'] = ('415560', 'COLL NEW ROCHELLE-ROSA PK', False)
known_institutions['415000'] = ('415000', 'COLLEGE MOUNT ST VINCENT', False)
known_institutions['416500'] = ('416500', 'COLLEGE OF SAINT ROSE', False)
known_institutions['513500'] = ('513500', 'COLLEGE OF WESTCHESTER', False)
known_institutions['418000'] = ('418000', 'COLUMBIA UNIVERSITY', False)
known_institutions['271500'] = ('271500', 'COLUMBIA-GREENE COMM COLL', False)
known_institutions['608000'] = ('608000', 'COMMUNITY GEN HOSP SYR', False)
known_institutions['418500'] = ('418500', 'CONCORDIA COLLEGE', False)
known_institutions['419000'] = ('419000', 'COOPER UNION', False)
known_institutions['419510'] = ('419510', 'CORNELL UNIVERSITY', False)
known_institutions['419530'] = ('419530', 'CORNELLNYC TECH', False)
known_institutions['272100'] = ('272100', 'CORNING COMM COLL', False)
known_institutions['606100'] = ('606100', 'CTR NAT WELL SCH MASS THE', False)
known_institutions['420000'] = ('420000', 'CULINARY INSTITUTE AMER', False)
known_institutions['330500'] = ('330500', 'CUNY BARUCH COLLEGE', False)
known_institutions['331000'] = ('331000', 'CUNY BROOKLYN COLL', False)
known_institutions['331500'] = ('331500', 'CUNY CITY COLLEGE', False)
known_institutions['331800'] = ('331800', 'CUNY COLL STATEN ISLAND', False)
known_institutions['310500'] = ('310500', 'CUNY GRADUATE SCHOOL', False)
known_institutions['332500'] = ('332500', 'CUNY HUNTER COLLEGE', False)
known_institutions['333000'] = ('333000', 'CUNY JOHN JAY COLLEGE', False)
known_institutions['311000'] = ('311000', 'CUNY LAW SCHOOL AT QUEENS', False)
known_institutions['332000'] = ('332000', 'CUNY LEHMAN COLLEGE', False)
known_institutions['334000'] = ('334000', 'CUNY QUEENS COLLEGE', False)
known_institutions['310510'] = ('310510', 'CUNY SCHOOL OF PROF STUDY', False)
known_institutions['335000'] = ('335000', 'CUNY YORK COLLEGE', False)
known_institutions['609000'] = ('609000', 'CURTIS HIGH SCHOOL', False)
known_institutions['422000'] = ('422000', 'D\'YOUVILLE COLLEGE', False)
known_institutions['420500'] = ('420500', 'DAEMEN COLLEGE', False)
known_institutions['420510'] = ('420510', 'DAEMEN COLLEGE-BROOKLYN', False)
known_institutions['458300'] = ('458300', 'DAVIS COLLEGE', False)
known_institutions['609200'] = ('609200', 'DEL-CHEN-MAD-OTSEGO BOCES', False)
known_institutions['504520'] = ('504520', 'DEVRY COLLEGE OF NEW YORK', False)
known_institutions['421000'] = ('421000', 'DOMINICAN COLL BLAUVELT', False)
known_institutions['448200'] = ('448200', 'DOROTHEA HOPFER SCH NURSI', False)
known_institutions['421510'] = ('421510', 'DOWLING COLL - BROOKHAVEN', False)
known_institutions['421500'] = ('421500', 'DOWLING COLLEGE', False)
known_institutions['272400'] = ('272400', 'DUTCHESS COMM COLL', False)
known_institutions['610000'] = ('610000', 'DUTCHESS COUNTY BOCES', False)
known_institutions['623500'] = ('623500', 'EASTERN SUFFOLK BOCES', False)
known_institutions['611500'] = ('611500', 'EDUC OPP CTR AT SUNY BUFF', False)
known_institutions['611000'] = ('611000', 'EDUC OPPORTUNITY CENTER', False)
known_institutions['423400'] = ('423400', 'ELIM BIBLE INST & COLLEGE', False)
known_institutions['504600'] = ('504600', 'ELITE ACAD MASSGE THERAPY', False)
known_institutions['423200'] = ('423200', 'ELLIS MED-BELANGER SCHOOL', False)
known_institutions['504410'] = ('504410', 'ELMIRA BUS INST - VESTAL', False)
known_institutions['504400'] = ('504400', 'ELMIRA BUSINESS INSTITUTE', False)
known_institutions['423500'] = ('423500', 'ELMIRA COLLEGE', False)
known_institutions['423600'] = ('423600', 'ELYON COLLEGE', False)
known_institutions['612500'] = ('612500', 'ERIE CO BOCES-FIRST DIST', False)
known_institutions['272710'] = ('272710', 'ERIE COMM COLL - CITY', False)
known_institutions['272700'] = ('272700', 'ERIE COMM COLL - NORTH', False)
known_institutions['272720'] = ('272720', 'ERIE COMM COLL - SOUTH', False)
known_institutions['606500'] = ('606500', 'ERIE II-CHAUT-CATTA BOCES', False)
known_institutions['510000'] = ('510000', 'EVEREST INSTITUTE', False)
known_institutions['459200'] = ('459200', 'EXCELSIOR COLLEGE', False)
known_institutions['273000'] = ('273000', 'FASHION INST OF TECH', False)
known_institutions['424110'] = ('424110', 'FEI TIAN - MIDDLETOWN', False)
known_institutions['424100'] = ('424100', 'FEI TIAN COLLEGE', False)
known_institutions['271800'] = ('271800', 'FINGER LAKES COMM COL', False)
known_institutions['612710'] = ('612710', 'FINGER LAKES SCHL/MASSAGE', False)
known_institutions['612700'] = ('612700', 'FINGER LAKES SCHL/MASSAGE', False)
known_institutions['424200'] = ('424200', 'FINGERLAKE HLTH CON&H SCI', False)
known_institutions['505000'] = ('505000', 'FIVE TOWNS COLLEGE', False)
known_institutions['424530'] = ('424530', 'FORDHAM UNIV-WESTCHESTER', False)
known_institutions['424500'] = ('424500', 'FORDHAM(RSE HILL-LNCLN C)', False)
known_institutions['273300'] = ('273300', 'FULTON-MONTGOMERY COMM C', False)
known_institutions['425300'] = ('425300', 'GAMLA COLLEGE', False)
known_institutions['613200'] = ('613200', 'GEN-LIV-STEUB-WYOM BOCES', False)
known_institutions['425500'] = ('425500', 'GENERAL THEOLOGICAL SEM', False)
known_institutions['273600'] = ('273600', 'GENESEE COMM COLL', False)
known_institutions['630140'] = ('630140', 'GESTALT ASSOC FOR PSYCHO', False)
known_institutions['613400'] = ('613400', 'GESTALT CTR PSYCHOTHERAPY', False)
known_institutions['425600'] = ('425600', 'GLASGOW CALEDONIAN NY COL', False)
known_institutions['505100'] = ('505100', 'GLOBE INST OF TECH, INC', False)
known_institutions['426500'] = ('426500', 'HAMILTON COLLEGE', False)
known_institutions['613500'] = ('613500', 'HAMILTON-FULTN-MONT BOCES', False)
known_institutions['614000'] = ('614000', 'HARLEM HOSPITAL CENTER', False)
known_institutions['427500'] = ('427500', 'HARTWICK COLLEGE', False)
known_institutions['428000'] = ('428000', 'HEBREW UNION COLLEGE', False)
known_institutions['428500'] = ('428500', 'HELENE FULD COL NURSING', False)
known_institutions['615500'] = ('615500', 'HERKIMER COUNTY BOCES', False)
known_institutions['273900'] = ('273900', 'HERKIMER COUNTY COMM COLL', False)
known_institutions['429000'] = ('429000', 'HILBERT COLLEGE', False)
known_institutions['616000'] = ('616000', 'HILLCREST HIGH SCHOOL', False)
known_institutions['429500'] = ('429500', 'HOBART-WILLIAM SMITH COLL', False)
known_institutions['430000'] = ('430000', 'HOFSTRA UNIVERSITY-MAIN', False)
known_institutions['430500'] = ('430500', 'HOLY TRINITY ORTHODOX SEM', False)
known_institutions['616500'] = ('616500', 'HOSP SPECIAL SURGERY NRSG', False)
known_institutions['371500'] = ('371500', 'HOSTOS COMM COLL', False)
known_institutions['431000'] = ('431000', 'HOUGHTON COLLEGE', False)
known_institutions['274200'] = ('274200', 'HUDSON VALLEY COMM COLL', False)
known_institutions['616510'] = ('616510', 'HUDSON VALLEY SCH MASS TH', False)
known_institutions['505300'] = ('505300', 'HUNTER BUSINESS SCHOOL', False)
known_institutions['448000'] = ('448000', 'ICAHN SCHLOFMED @ MTSINAI', False)
known_institutions['432500'] = ('432500', 'INST DESIGN & CONSTRUCT', False)
known_institutions['630405'] = ('630405', 'INST FOR CONTEMP PSYCHO', False)
known_institutions['630410'] = ('630410', 'INST FOR EXPRESSIVE ANALY', False)
known_institutions['630530'] = ('630530', 'INST FOR PSY TRNG & RSRCH', False)
known_institutions['616750'] = ('616750', 'INST FOR PSYCHOANLYTIC ED', False)
known_institutions['630110'] = ('630110', 'INT SCH FOR MENT HLTH PRA', False)
known_institutions['616800'] = ('616800', 'INT\'NTL COL / ACUPUNCTURE', False)
known_institutions['505500'] = ('505500', 'INTERBORO INSTITUTE', False)
known_institutions['433100'] = ('433100', 'IONA COL-NEW ROCHELLE CAM', False)
known_institutions['433120'] = ('433120', 'IONA-ROCKLAND CAMPUS', False)
known_institutions['617000'] = ('617000', 'ISABELLA G HART SCH NRSG', False)
known_institutions['505600'] = ('505600', 'ISLAND DRAFT & TECH INST', False)
known_institutions['433500'] = ('433500', 'ITHACA COLLEGE', False)
known_institutions['505700'] = ('505700', 'ITT TECH - ALBANY', False)
known_institutions['505800'] = ('505800', 'ITT TECH - GETZVILLE', False)
known_institutions['505900'] = ('505900', 'ITT TECH - LIVERPOOL', False)
known_institutions['506000'] = ('506000', 'JAMESTOWN BUSINESS COLL', False)
known_institutions['274510'] = ('274510', 'JAMESTOWN CC-CATTARAUGUS', False)
known_institutions['274500'] = ('274500', 'JAMESTOWN COMM COLL', False)
known_institutions['618500'] = ('618500', 'JEF-LEW-HAM-HERK-ONEI BOC', False)
known_institutions['274800'] = ('274800', 'JEFFERSON COMM COLL', False)
known_institutions['434000'] = ('434000', 'JEWISH THEOLOGICAL SEM', False)
known_institutions['434500'] = ('434500', 'JUILLIARD SCHOOL (THE)', False)
known_institutions['620100'] = ('620100', 'JUNGIAN PSYCHOANLYTC ASSC', False)
known_institutions['507000'] = ('507000', 'KATHARINE GIBBS-NYC', False)
known_institutions['435010'] = ('435010', 'KEUKA - ONONDAGA CC', False)
known_institutions['435020'] = ('435020', 'KEUKA COLL-CORNING CC CAM', False)
known_institutions['435000'] = ('435000', 'KEUKA COLLEGE', False)
known_institutions['435500'] = ('435500', 'KING\'S COLLEGE (THE)', False)
known_institutions['620200'] = ('620200', 'KINGS CO HOSP-SCH ANESTH', False)
known_institutions['372500'] = ('372500', 'KINGSBOROUGH COMM COLL', False)
known_institutions['438000'] = ('438000', 'L.I. COLL HOSP SCH NRSNG', False)
known_institutions['372000'] = ('372000', 'LA GUARDIA COMM COLL', False)
known_institutions['507500'] = ('507500', 'LAB INST MERCHANDISING', False)
known_institutions['437500'] = ('437500', 'LE MOYNE COLLEGE', False)
known_institutions['803189'] = ('803189', 'LEBANESE AMER UNIV-BYBLOS', False)
known_institutions['803289'] = ('803289', 'LEBANESE AMER UNIV-SIDON', False)
known_institutions['803089'] = ('803089', 'LEBANESE AMERICAN UNIV', False)
known_institutions['620300'] = ('620300', 'LENOX HILL HOSPITAL', False)
known_institutions['438500'] = ('438500', 'LIU - CENTRAL ADMIN', False)
known_institutions['438510'] = ('438510', 'LIU BROOKLYN CAMPUS', False)
known_institutions['438530'] = ('438530', 'LIU SOUTHAMPTON CAMPUS', False)
known_institutions['438523'] = ('438523', 'LIU-BRENTWOOD CAMPUS', False)
known_institutions['438520'] = ('438520', 'LIU-C W POST CAMPUS', False)
known_institutions['438511'] = ('438511', 'LIU-HUDSN GRADCTR WESTCHR', False)
known_institutions['438540'] = ('438540', 'LIU-NEW YORK UNIV CAMPUS', False)
known_institutions['507810'] = ('507810', 'LONG ISL BUS INST-FLUSH', False)
known_institutions['507800'] = ('507800', 'LONG ISLAND BUSINESS INST', False)
known_institutions['438550'] = ('438550', 'LONG ISLAND U-RIVERHEAD', False)
known_institutions['470600'] = ('470600', 'LOUIS V GERSTNER GRAD SCH', False)
known_institutions['000102'] = ('000102', 'LUISS LIBERA UNIVERSITA', False)
known_institutions['622000'] = ('622000', 'MADISON-ONEIDA BOCES', False)
known_institutions['507900'] = ('507900', 'MANDL SCHOOL', False)
known_institutions['439000'] = ('439000', 'MANHATTAN COLLEGE', False)
known_institutions['622550'] = ('622550', 'MANHATTAN INST PSYCHANLYS', False)
known_institutions['439500'] = ('439500', 'MANHATTAN SCHOOL OF MUSIC', False)
known_institutions['440000'] = ('440000', 'MANHATTANVILLE COLLEGE', False)
known_institutions['441000'] = ('441000', 'MARIA COLLEGE OF ALBANY', False)
known_institutions['622500'] = ('622500', 'MARION S WHELAN SCH NRSG', False)
known_institutions['442000'] = ('442000', 'MARIST COLLEGE', False)
known_institutions['443500'] = ('443500', 'MARYMOUNT MANHATTAN COLL', False)
known_institutions['444520'] = ('444520', 'MEDAILLE COLL-ROCHESTER', False)
known_institutions['444500'] = ('444500', 'MEDAILLE COLLEGE', False)
known_institutions['444510'] = ('444510', 'MEDAILLE COLLEGE-AMHERST', False)
known_institutions['372800'] = ('372800', 'MEDGAR EVERS COLL', False)
known_institutions['444600'] = ('444600', 'MEMORIAL COLLEGE OF NRSG', False)
known_institutions['623000'] = ('623000', 'MEMORIAL HOSPITAL', False)
known_institutions['445020'] = ('445020', 'MERCY COL - BRONX CAMPUS', False)
known_institutions['445060'] = ('445060', 'MERCY COLL-MANHATTAN CAMP', False)
known_institutions['445010'] = ('445010', 'MERCY COLL-YORKTOWN HGHTS', False)
known_institutions['445000'] = ('445000', 'MERCY COLLEGE-MAIN', False)
known_institutions['630420'] = ('630420', 'MET INS FOR TRN N PSY PSY', False)
known_institutions['414000'] = ('414000', 'METROPOLITAN COLL OF NY', False)
known_institutions['414010'] = ('414010', 'METROPOLITAN COLL.-NY-BRC', False)
known_institutions['507600'] = ('507600', 'MILDRED ELLEY SCHOOL', False)
known_institutions['507610'] = ('507610', 'MILDRED ELLEY-NYC', False)
known_institutions['275110'] = ('275110', 'MOHAWK VALLEY CC-ROME', False)
known_institutions['275100'] = ('275100', 'MOHAWK VALLEY COMM COLL', False)
known_institutions['446500'] = ('446500', 'MOLLOY COLLEGE', False)
known_institutions['508010'] = ('508010', 'MONROE COLL-NEW ROCHELLE', False)
known_institutions['508000'] = ('508000', 'MONROE COLLEGE', False)
known_institutions['275410'] = ('275410', 'MONROE COM COL-DOWNTOWN', False)
known_institutions['275400'] = ('275400', 'MONROE COMM COLL', False)
known_institutions['620320'] = ('620320', 'MONROE 2 - ORLEANS BOCES', False)
known_institutions['446600'] = ('446600', 'MONTEFIORE SCHL OF NURSNG', False)
known_institutions['447500'] = ('447500', 'MOUNT SAINT MARY COLLEGE', False)
known_institutions['624900'] = ('624900', 'MOUNT SINAI HOSPITAL', False)
known_institutions['275700'] = ('275700', 'NASSAU COMM COLL', False)
known_institutions['625500'] = ('625500', 'NASSAU COUNTY BOCES', False)
known_institutions['000106'] = ('000106', 'NAT CHUNG-HSING UNIV', False)
known_institutions['630800'] = ('630800', 'NAT\'L INST PSYCHOTHERAPY', False)
known_institutions['000103'] = ('000103', 'NATIONAL CHIAO TUNG UNIV', False)
known_institutions['630510'] = ('630510', 'NATL PSYCH ASSC PSYCHANLY', False)
known_institutions['448500'] = ('448500', 'NAZARETH COLL ROCHESTER', False)
known_institutions['510800'] = ('510800', 'NEW YORK CAREER INSTITUTE', False)
known_institutions['451000'] = ('451000', 'NEW YORK LAW SCHOOL', False)
known_institutions['451500'] = ('451500', 'NEW YORK MEDICAL COLLEGE', False)
known_institutions['453000'] = ('453000', 'NEW YORK UNIVERSITY-MAIN', False)
known_institutions['276000'] = ('276000', 'NIAGARA COUNTY COMM COLL', False)
known_institutions['453500'] = ('453500', 'NIAGARA UNIVERSITY', False)
known_institutions['276310'] = ('276310', 'NORTH CO CC-ELIZABETHTOWN', False)
known_institutions['276320'] = ('276320', 'NORTH CO CC-MALONE', False)
known_institutions['276330'] = ('276330', 'NORTH CO CC-TICONDEROGA', False)
known_institutions['276300'] = ('276300', 'NORTH COUNTRY COMM COLL', False)
known_institutions['454000'] = ('454000', 'NORTHEASTERN SEMINARY', False)
known_institutions['449500'] = ('449500', 'NY CHIROPRACTIC COLLEGE', False)
known_institutions['448700'] = ('448700', 'NY COLL OF HLTH PROFESSIO', False)
known_institutions['450100'] = ('450100', 'NY COLL OF TRAD CHINE MED', False)
known_institutions['450000'] = ('450000', 'NY COLL PODIATRIC MED', False)
known_institutions['512300'] = ('512300', 'NY CONSRVTRY DRAMATIC ART', False)
known_institutions['407300'] = ('407300', 'NY GRAD SCHOOL  PSYCHOAN', False)
known_institutions['630400'] = ('630400', 'NY INST FOR PSYC SELF PSY', False)
known_institutions['450520'] = ('450520', 'NY INST TECH-MANHATTAN', False)
known_institutions['450530'] = ('450530', 'NY INST TECH-OLD WESTBURY', False)
known_institutions['626300'] = ('626300', 'NY INSTITUTE OF MASSAGE', False)
known_institutions['626460'] = ('626460', 'NY PSYCHANLYTC SOC & INST', False)
known_institutions['623350'] = ('623350', 'NY SCH MED&DENT ASSTS INC', False)
known_institutions['452000'] = ('452000', 'NY SCHOOL INTERIOR DESIGN', False)
known_institutions['449100'] = ('449100', 'NY STUDIO SCHOOL', False)
known_institutions['452500'] = ('452500', 'NY THEOLOGICAL SEMINARY', False)
known_institutions['454500'] = ('454500', 'NYACK COLLEGE', False)
known_institutions['508100'] = ('508100', 'NYADI', False)
known_institutions['333800'] = ('333800', 'NYC COLLEGE OF TECHNOLOGY', False)
known_institutions['623300'] = ('623300', 'NYC DEPT OF EDUCATION', False)
known_institutions['512400'] = ('512400', 'NYFA', False)
known_institutions['250030'] = ('250030', 'NYS SCH INDUS & LABOR REL', False)
known_institutions['250010'] = ('250010', 'NYSC AG & LIFE SCIENCES', False)
known_institutions['251000'] = ('251000', 'NYSC CERAMICS-ALFRED', False)
known_institutions['250020'] = ('250020', 'NYSC HUMAN ECOLOGY', False)
known_institutions['250040'] = ('250040', 'NYSC VETERINARY MEDICINE', False)
known_institutions['110000'] = ('110000', 'NYSDOH WADSWORTH CENTER', False)
known_institutions['453030'] = ('453030', 'NYU @ ST. THOMAS AQUINAS', False)
known_institutions['453100'] = ('453100', 'NYU LONG ISLAND SCH-MED.', False)
known_institutions['627500'] = ('627500', 'ONEIDA-MADISON-HERK BOCES', False)
known_institutions['276600'] = ('276600', 'ONONDAGA COMM COLL', False)
known_institutions['620410'] = ('620410', 'ONONDAGA SCH THER MASSAGE', False)
known_institutions['620400'] = ('620400', 'ONONDAGA SCH THER MASSAGE', False)
known_institutions['628000'] = ('628000', 'ONONDAGA-CORT-MADIS BOCES', False)
known_institutions['276900'] = ('276900', 'ORANGE COUNTY COMM COLL', False)
known_institutions['276910'] = ('276910', 'ORANGE CTY CC-NEWBURGH', False)
known_institutions['628500'] = ('628500', 'ORANGE-ULSTER CNTY BOCES', False)
known_institutions['629000'] = ('629000', 'ORLEANS-NIAGARA BOCES', False)
known_institutions['629500'] = ('629500', 'OSWEGO COUNTY BOCES', False)
known_institutions['630000'] = ('630000', 'OTSE-DELA-SCHO-GRE-BOCES', False)
known_institutions['455520'] = ('455520', 'PACE UNIV-PLEASANTVILLE', False)
known_institutions['455530'] = ('455530', 'PACE UNIV-WHITE PLAINS', False)
known_institutions['455510'] = ('455510', 'PACE UNIVERSITY-NEW YORK', False)
known_institutions['509100'] = ('509100', 'PACIFIC COLL ORIENTAL MED', False)
known_institutions['457500'] = ('457500', 'PAUL SMITH\'S COLLEGE', False)
known_institutions['406500'] = ('406500', 'PHILLIPS BETH ISRAEL NRSG', False)
known_institutions['509300'] = ('509300', 'PLAZA COLLEGE', False)
known_institutions['458010'] = ('458010', 'POLYTECH INST OF NYU-LI', False)
known_institutions['458020'] = ('458020', 'POLYTECH INST OF NYU-WEST', False)
known_institutions['419800'] = ('419800', 'POMEROY CON @ CROUSE HOSP', False)
known_institutions['458500'] = ('458500', 'PRATT INSTITUTE', False)
known_institutions['458510'] = ('458510', 'PRATT MANHATTAN CENTER', False)
known_institutions['630520'] = ('630520', 'PRIMARY STAGES', False)
known_institutions['458700'] = ('458700', 'PROFESSIONAL BUS COLL', False)
known_institutions['648000'] = ('648000', 'PSY TR INST CNTMP FDN SOC', False)
known_institutions['630300'] = ('630300', 'PSYCHANLYT PSYCHTHPY ST C', False)
known_institutions['631000'] = ('631000', 'PUTNAM-WESTCHESTER BOCES', False)
known_institutions['373500'] = ('373500', 'QUEENSBOROUGH COMM COLL', False)
known_institutions['459000'] = ('459000', 'RABBI ISAAC ELCHANAN SEM', False)
known_institutions['459300'] = ('459300', 'RELAY GRAD SCHOOL OF EDUC', False)
known_institutions['632000'] = ('632000', 'RENSS-COLUMB-GREENE BOCES', False)
known_institutions['459500'] = ('459500', 'RENSSELAER POLYTECH INST', False)
known_institutions['460000'] = ('460000', 'ROBERTS WESLEYAN COLLEGE', False)
known_institutions['460500'] = ('460500', 'ROCHESTER INST TECHNOLOGY', False)
known_institutions['461000'] = ('461000', 'ROCKEFELLER UNIVERSITY', False)
known_institutions['277200'] = ('277200', 'ROCKLAND COMM COLL', False)
known_institutions['633000'] = ('633000', 'ROCKLAND COUNTY BOCES', False)
known_institutions['800877'] = ('800877', 'SACKLER SCH OF MEDICINE', False)
known_institutions['468600'] = ('468600', 'SALVATION ARMY SCHOOL', False)
known_institutions['468700'] = ('468700', 'SAMARITAN HOSP SCHL NURS', False)
known_institutions['639550'] = ('639550', 'SAMFORD UNIVERSITY', False)
known_institutions['469000'] = ('469000', 'SARAH LAWRENCE COLLEGE', False)
known_institutions['506500'] = ('506500', 'SBI CAMPUS-SANFORD BROWN', False)
known_institutions['277500'] = ('277500', 'SCHENECTADY COUNTY COMM C', False)
known_institutions['510500'] = ('510500', 'SCHOOL OF VISUAL ARTS', False)
known_institutions['640510'] = ('640510', 'SCHU-STEU-CHE-TIO-ALL-BOC', False)
known_institutions['642000'] = ('642000', 'SCHUY-STEU-CHEM-TIO BOCES', False)
known_institutions['640500'] = ('640500', 'SCHUYLER-CHEM-TIOGA BOCES', False)
known_institutions['000101'] = ('000101', 'SDA BOCCONI', False)
known_institutions['469500'] = ('469500', 'SEM IMMACULATE CONCEPTION', False)
known_institutions['470000'] = ('470000', 'SIENA COLLEGE', False)
known_institutions['510600'] = ('510600', 'SIMMONS INST FUNERAL SERV', False)
known_institutions['000100'] = ('000100', 'SINGIDUNUM UNIV-FEFA', False)
known_institutions['470500'] = ('470500', 'SKIDMORE COLLEGE', False)
known_institutions['510700'] = ('510700', 'SOTHEBY\'S INST OF ART-NY', False)
known_institutions['000104'] = ('000104', 'SOUTHEAST UNIVERSITY', False)
known_institutions['624000'] = ('624000', 'SOUTHERN WESTCHEST/BOCES', False)
known_institutions['463000'] = ('463000', 'ST BERNARD\'S SCH THEO&MIN', False)
known_institutions['463500'] = ('463500', 'ST BONAVENTURE UNIVERSITY', False)
known_institutions['464000'] = ('464000', 'ST ELIZ COLL OF NURSING', False)
known_institutions['464500'] = ('464500', 'ST FRANCIS COLLEGE', False)
known_institutions['634500'] = ('634500', 'ST FRANCIS HOSP NURSING', False)
known_institutions['635000'] = ('635000', 'ST JAMES MERCY HOSPITAL', False)
known_institutions['465000'] = ('465000', 'ST JOHN FISHER COLLEGE', False)
known_institutions['465530'] = ('465530', 'ST JOHN\'S UNIV-MANHATTAN', False)
known_institutions['465510'] = ('465510', 'ST JOHN\'S UNIV-STATEN IS', False)
known_institutions['465500'] = ('465500', 'ST JOHN\'S UNIVERSITY-MAIN', False)
known_institutions['466510'] = ('466510', 'ST JOSEPH\'S COLL-SUFFOLK', False)
known_institutions['466700'] = ('466700', 'ST JOSEPH\'S COLL-SYRACUSE', False)
known_institutions['466500'] = ('466500', 'ST JOSEPH\'S COLLEGE-MAIN', False)
known_institutions['467000'] = ('467000', 'ST JOSEPH\'S SEM & COLL', False)
known_institutions['467020'] = ('467020', 'ST JOSEPH\'S SEM&COLL-DOUG', False)
known_institutions['467010'] = ('467010', 'ST JOSEPH\'S SEM&COLL-HUNT', False)
known_institutions['467500'] = ('467500', 'ST LAWRENCE UNIVERSITY', False)
known_institutions['637000'] = ('637000', 'ST LAWRENCE-LEWIS BOCES', False)
known_institutions['510300'] = ('510300', 'ST PAULS SCHL NURS-QUEENS', False)
known_institutions['510310'] = ('510310', 'ST PAULS SCHL NURS-S.I.', False)
known_institutions['468000'] = ('468000', 'ST THOMAS AQUINAS COLLEGE', False)
known_institutions['468500'] = ('468500', 'ST VLADIMIR\'S THEO SEM', False)
known_institutions['467030'] = ('467030', 'ST. JOSEPH\'S-POUGHKEEPSIE', False)
known_institutions['411300'] = ('411300', 'ST. VINCENTS CATH MED CTR', False)
known_institutions['639000'] = ('639000', 'ST. VINCENTS CATH MED CTR', False)
known_institutions['468300'] = ('468300', 'ST. VINCENTS CATH MED CTR', False)
known_institutions['641500'] = ('641500', 'ST. VINCENTS CATHOLIC MED', False)
known_institutions['333500'] = ('333500', 'STELLA & CHAS GUTTMAN CC', False)
known_institutions['230500'] = ('230500', 'SUC BROCKPORT', False)
known_institutions['231000'] = ('231000', 'SUC BUFFALO', False)
known_institutions['231500'] = ('231500', 'SUC CORTLAND', False)
known_institutions['232500'] = ('232500', 'SUC FREDONIA', False)
known_institutions['233000'] = ('233000', 'SUC GENESEO', False)
known_institutions['233500'] = ('233500', 'SUC NEW PALTZ', False)
known_institutions['234000'] = ('234000', 'SUC OLD WESTBURY', False)
known_institutions['234500'] = ('234500', 'SUC ONEONTA', False)
known_institutions['235000'] = ('235000', 'SUC OSWEGO', False)
known_institutions['235010'] = ('235010', 'SUC OSWEGO-METRO CENTER', False)
known_institutions['235501'] = ('235501', 'SUC PLATTSBRG @ ACC', False)
known_institutions['235500'] = ('235500', 'SUC PLATTSBURGH', False)
known_institutions['236000'] = ('236000', 'SUC POTSDAM', False)
known_institutions['236500'] = ('236500', 'SUC PURCHASE', False)
known_institutions['277800'] = ('277800', 'SUFFOLK CNTY CC-AMMERMAN', False)
known_institutions['277810'] = ('277810', 'SUFFOLK COUNTY CC-EASTERN', False)
known_institutions['277820'] = ('277820', 'SUFFOLK COUNTY CC-WESTERN', False)
known_institutions['642200'] = ('642200', 'SULLIVAN COUNTY BOCES', False)
known_institutions['278100'] = ('278100', 'SULLIVAN COUNTY COMM COLL', False)
known_institutions['470800'] = ('470800', 'SUNBRIDGE COL', False)
known_institutions['210500'] = ('210500', 'SUNY ALBANY', False)
known_institutions['211000'] = ('211000', 'SUNY BINGHAMTON', False)
known_institutions['211500'] = ('211500', 'SUNY BUFFALO', False)
known_institutions['240500'] = ('240500', 'SUNY COL ENV SCI & FOREST', False)
known_institutions['241500'] = ('241500', 'SUNY COL OF OPTOMETRY', False)
known_institutions['232000'] = ('232000', 'SUNY EMPIRE STATE COLLEGE', False)
known_institutions['221000'] = ('221000', 'SUNY HLTH SCI CTR BRKLYN', False)
known_institutions['222000'] = ('222000', 'SUNY HLTH SCI CTR SYRACUS', False)
known_institutions['241000'] = ('241000', 'SUNY MARITIME COLLEGE', False)
known_institutions['240700'] = ('240700', 'SUNY POLYTECHNIC INST', False)
known_institutions['212000'] = ('212000', 'SUNY STONY BROOK', False)
known_institutions['261500'] = ('261500', 'SUNYC AG&TECH COBLESKILL', False)
known_institutions['263010'] = ('263010', 'SUNYC AG&TECH MOR-NORWICH', False)
known_institutions['263000'] = ('263000', 'SUNYC AG&TECH MORRISVILLE', False)
known_institutions['260500'] = ('260500', 'SUNYC TECH ALFRED', False)
known_institutions['260510'] = ('260510', 'SUNYC TECH ALFRED/WLLSVLE', False)
known_institutions['261000'] = ('261000', 'SUNYC TECH CANTON', False)
known_institutions['262000'] = ('262000', 'SUNYC TECH DELHI', False)
known_institutions['262010'] = ('262010', 'SUNYC TECH DELHI @ SCCC', False)
known_institutions['262500'] = ('262500', 'SUNYC TECH FARMINGDALE', False)
known_institutions['511200'] = ('511200', 'SWEDISH INSTITUTE, INC.', False)
known_institutions['642500'] = ('642500', 'SYRACUSE CITY SCHOOLS', False)
known_institutions['471000'] = ('471000', 'SYRACUSE UNIVERSITY', False)
known_institutions['471500'] = ('471500', 'TEACHERS COLLEGE', False)
known_institutions['512000'] = ('512000', 'TECHNICAL CAREER INSTS', False)
known_institutions['457700'] = ('457700', 'THE ELMEZZI G SC MOLEC MD', False)
known_institutions['614001'] = ('614001', 'THE HARLEM FAMILY INST', False)
known_institutions['449000'] = ('449000', 'THE NEW SCHOOL', False)
known_institutions['425700'] = ('425700', 'THE NEW YORK ACAD OF ART', False)
known_institutions['462020'] = ('462020', 'THE SAGE COL-ALBANY CAMP', False)
known_institutions['462000'] = ('462000', 'THE SAGE COL-TROY CAMPUS', False)
known_institutions['278400'] = ('278400', 'TOMPKINS-CORTLAND COMM C', False)
known_institutions['472030'] = ('472030', 'TOURO COLL - BAY SHORE', False)
known_institutions['472020'] = ('472020', 'TOURO COLL - FLATBUSH', False)
known_institutions['472000'] = ('472000', 'TOURO COLLEGE', False)
known_institutions['472070'] = ('472070', 'TOURO COLLEGE - VALHALLA', False)
known_institutions['472010'] = ('472010', 'TOURO COLLEGE-CENTR ISLIP', False)
known_institutions['472050'] = ('472050', 'TOURO COLLEGE-HARLEM', False)
known_institutions['472040'] = ('472040', 'TOURO COLLEGE-KEW GARDENS', False)
known_institutions['472060'] = ('472060', 'TOURO COLLEGE-MIDDLETOWN', False)
known_institutions['515500'] = ('515500', 'TRANSITIONS CAREER INST', False)
known_institutions['512600'] = ('512600', 'TRI-STATE COLL OF ACUPUNC', False)
known_institutions['472500'] = ('472500', 'TROCAIRE COLLEGE', False)
known_institutions['643500'] = ('643500', 'ULSTER COUNTY BOCES', False)
known_institutions['279000'] = ('279000', 'ULSTER COUNTY COMM COLL', False)
known_institutions['472800'] = ('472800', 'UNIFICATION THEO SEMINARY', False)
known_institutions['473000'] = ('473000', 'UNION COLLEGE', False)
known_institutions['426100'] = ('426100', 'UNION GRADUATE COLLEGE', False)
known_institutions['473500'] = ('473500', 'UNION THEOLOGICAL SEM', False)
known_institutions['000105'] = ('000105', 'UNIVERSIDAD ALBERTO HURTA', False)
known_institutions['474000'] = ('474000', 'UNIVERSITY OF ROCHESTER', False)
known_institutions['474300'] = ('474300', 'UTICA COLLEGE', False)
known_institutions['513010'] = ('513010', 'UTICA SCHL COMMERCE-CANAS', False)
known_institutions['513020'] = ('513020', 'UTICA SCHL COMMERCE-ONEON', False)
known_institutions['513000'] = ('513000', 'UTICA SCHOOL OF COMMERCE', False)
known_institutions['474500'] = ('474500', 'VASSAR COLLEGE', False)
known_institutions['400500'] = ('400500', 'VAUGHN COLL OF AERO & TEC', False)
known_institutions['475500'] = ('475500', 'VILLA MARIA COLLEGE BUFF', False)
known_institutions['645000'] = ('645000', 'VOC ED NASSAU COUNTY NRSG', False)
known_institutions['477000'] = ('477000', 'WAGNER COLLEGE', False)
known_institutions['645300'] = ('645300', 'WASH-SARA-WAREN-HAMIL-ESS', False)
known_institutions['630700'] = ('630700', 'WASHINGTON SQ INSTITUTE', False)
known_institutions['645500'] = ('645500', 'WAYNE-FINGER LAKES BOCES', False)
known_institutions['477500'] = ('477500', 'WEBB INSTITUTE', False)
known_institutions['419520'] = ('419520', 'WEILL CORNELL MEDCOL&GSMS', False)
known_institutions['478000'] = ('478000', 'WELLS COLLEGE', False)
known_institutions['279300'] = ('279300', 'WESTCHESTER COMM COLL', False)
known_institutions['630540'] = ('630540', 'WESTCHESTER INST FOR TRNG', False)
known_institutions['621000'] = ('621000', 'WESTERN SUFFOLK BOCES', False)
known_institutions['630150'] = ('630150', 'WM. ALANSON WHITE INST', False)
known_institutions['514000'] = ('514000', 'WOOD/TOBE-COBURN SCHOOL', False)
known_institutions['479000'] = ('479000', 'YESHIVA UNIVERSITY', False)
