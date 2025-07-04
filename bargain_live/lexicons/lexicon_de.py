class Lexicon:


    #-----------------------------------
    # Consent
    #-----------------------------------

    consent_title = "Herzlich Willkommen!"


    match_value = "In diesem Match beträgt dein Wert des Objekts "
    buyer_value_random = "Der Wert des Objekts für den Käufer wird zufällig zwischen 0 und 60€ gezogen."
    bargaining_starts_in = "Das Verhandeln beginnt in 5"
    negotiation_costs = "Verhandlungskosten"
    current_negotiation_costs = "Aktuelle Verhandlungskosten pro Sekunde: "
    total_negotiation_costs = "Gesamte Verhandlungskosten: "
    time = "Zeit: "
    current_price_offer = "Ihr aktuell abgegebenes Preisangebot: "
    no_offer_yet = "Noch kein Angebot."
    your_payoff = "Ihr Gewinn: "
    submit = "Absenden"
    instructions = "Erklärung"

    #-----------------------------------
    # Instructions
    #-----------------------------------



    welcome_message = "Die Auszahlung, die Sie aus diesem Experiment erhalten, hängt teilweise von Ihren Entscheidungen, teilweise von den Entscheidungen anderer und teilweise vom Zufall ab. Den Betrag, den Sie verdienen, erhalten Sie via "
    experiment_structure = "Das Experiment besteht aus 30 Runden, in denen Sie mit einer anderen Person verhandeln. Zu Beginn des Experiments wird den Teilnehmenden zufällig die Rolle des Käufers oder des Verkäufers zugewiesen. Die Rolle bleibt <b>über alle 30 Runden hinweg gleich</b>. Zu Beginn jeder Runde werden Sie zufällig einer anderen Person mit der anderen Rolle zugeordnet. Nach jeder Runde werden neue Paare gebildet."
    negotiation_intro = "In jeder Runde verhandeln Käufer und Verkäufer über ein Objekt:"

    buyer_value_one_sided = "Der Wert des Objekts für den Käufer ist jede Runde eine neue Zufallszahl zwischen 0 und 30 Euro."
    buyer_value_two_sided = "Der Wert des Objekts für den Käufer ist jede Runde eine neue Zufallszahl zwischen <b>0 und 60 Euro</b>."
    seller_value_one_sided = "Der Wert des Objekts für den Verkäufer <b>beträgt immer 0 Euro</b>."
    seller_value_two_sided = "Der Wert des Objekts für den Verkäufer ist auch eine Zufallszahl zwischen <b>0 und 60 Euro</b>."
    information_one_sided = "Der Verkäufer kennt den Wert des Objekts für den Käufer <b>nicht</b>."
    information_two_sided = "Keiner in der Verhandlung kennt den Wert des Objekts vom anderen."
    
    price_negotiation_heading = "Preisverhandlung"
    price_negotiation_intro = "Der Käufer und der Verkäufer verhandeln über den Preis:"
    price_submission = "Beide Teilnehmer können Preise vorschlagen, indem sie einen Wert auf einem Schieberegler auswählen und auf \"Absenden\" klicken."
    price_update = "Sie können während der Verhandlung jederzeit neue Preise vorschlagen. Wenn ein neuer Preis vorgeschlagen wird, wird der vorherige ungültig."
    costs_heading = "Kosten durch Verzögerung"
    costs_intro = "Während der Preisverhandlung entstehen zwei Arten von Kosten: Verhandlungskosten und Kosten durch Verzögerung."
    negotiation_cost_heading = "Verhandlungskosten"
    negotiation_costs1 = "Für jede Sekunde der Verhandlung fallen Verhandlungskosten in Höhe von "
    negotiation_costs2 = " Cent an. Je länger die Verhandlung dauert, desto höher sind die Kosten für beide Teilnehmenden. Die Summe der Verhandlungskosten wird von Ihrer Teilnahmevergütung abgezogen (die später noch erklärt wird)."
    termination_heading = "Kosten durch Verzögerung"
    termination_probability1 = "In jeder Sekunde der Verhandlung besteht eine "
    termination_probability2 = "-prozentige Wahrscheinlichkeit, dass der Computer die Verhandlung beendet. Im Durchschnitt bedeutet dies, dass Verhandlungen, wenn keine Einigung erzielt wird, etwa "
    termination_probability3 = " Sekunden dauern bevor sie vom Computer beendet werden."


    ending_negotiation_heading = "Die Verhandlung beenden"
    ending_negotiation_intro = "Die Verhandlung kann auf drei Arten enden:"
    acceptance_rule = "Wenn ein Teilnehmer das Preisangebot des anderen annimmt. Sie können ein Angebot auch durch ein \"dummes\" eigenes Angebot akzeptieren. Das bedeutet, wenn der Käufer ein Angebot macht, das über dem des Verkäufers liegt, wird dies als Annahme gewertet. Ebenso gilt: Wenn der Verkäufer ein Angebot macht, das unter dem des Käufers liegt, wird dies ebenfalls als Annahme gewertet."
    terminate_rule = "Wenn ein Teilnehmer auf \"Beenden\" klickt, wodurch die Verhandlung ohne Handelsgewinne für beide endet."
    
    termination_explanation_costs = "Bereits angefallene Verhandlungskosten bleiben jedoch bestehen."
    random_termination_rule = "Wenn die Verhandlung zufällig durch den Computer beendet wird, wodurch die Runde ohne Handelsgewinne für beide endet."
    random_termination_explanation_costs = "Bereits angefallene Verhandlungskosten bleiben jedoch bestehen."

    options_summary_heading = "Zusammenfassung der Optionen"
    options_summary_intro = "Während der Verhandlung haben Sie drei Möglichkeiten:"
    option_submit_price = "Einen neuen Preis vorschlagen."
    option_terminate = "Die Verhandlung beenden."
    option_accept = "Das Preisangebot des anderen Teilnehmers akzeptieren (erst verfügbar, nachdem das erste Angebot gemacht wurde)."
    example_buyer_screen = "Beispiel für die Käuferansicht"
    example_seller_screen = "Beispiel für die Verkäuferansicht"
    payment_heading = "Bezahlung"
    payment_info = "Am Ende des Experiments wird eine Runde zufällig für die Auszahlung ausgewählt. Ihre Auszahlung ergibt sich auf folgende Weise:"
    final_payoff_formula_ta_costs = "Endgültige Auszahlung = Teilnahmevergütung (10€) + Handelsgewinne – Verhandlungskosten"
    final_payoff_formula_no_ta_costs = "Endgültige Auszahlung = Teilnahmevergütung (10€) + Handelsgewinne"

    buyer_payoff_example_intro_transaction_costs = "Hier ist ein Beispiel dafür, wie die endgültige Auszahlung des Käufers berechnet wird: Wenn der ausgehandelte Preis 31€ beträgt, der Wert 38€ ist und Sie nach 20 Sekunden eine Einigung erzielen, ergibt sich folgende Auszahlung:"
    buyer_payoff_example_intro_no_transaction_costs = "Hier ist ein Beispiel dafür, wie die endgültige Auszahlung des Käufers berechnet wird: Wenn der ausgehandelte Preis 31€ beträgt, der Wert 38€ ist und Sie nach 20 Sekunden eine Einigung erzielen, ergibt sich folgende Auszahlung:"
    buyer_payoff_value = "Wert des Objekts: "
    buyer_payoff_price = "Preis: "
    buyer_payoff_trade_gains = "Handelsgewinne: "
    buyer_payoff_transaction_costs = "Verhandlungskosten: "
    buyer_payoff_match = "Gewinn aus der Runde: "
    buyer_payoff_participation_fee = "Teilnahmevergütung: "
    buyer_payoff_total = "Gesamtauszahlung: "

    seller_payoff_example_intro_transaction_costs = "Hier ist ein Beispiel, wie die Auszahlung des Verkäufers berechnet wird: Wenn der ausgehandelte Preis 20€ beträgt, der Wert 0€ ist und Sie nach 20 Sekunden eine Einigung erzielen, ergibt sich folgende Auszahlung:"
    seller_payoff_example_intro_no_transaction_costs = "Hier ist ein Beispiel, wie die Auszahlung des Verkäufers berechnet wird: Wenn der ausgehandelte Preis 20€ beträgt, der Wert 5€ ist und Sie nach 20 Sekunden eine Einigung erzielen, ergibt sich folgende Auszahlung:"
    seller_payoff_price = "Preis: "
    seller_payoff_value = "Wert des Objekts: "
    seller_payoff_trade_gains = "Handelsgewinne: "
    seller_payoff_transaction_costs = "Transaktionskosten: "
    seller_payoff_match = "Gewinn aus der Runde: "
    seller_payoff_participation_fee = "Teilnahmevergütung: "
    seller_payoff_total = "Gesamtauszahlung: "

    comprehension_question_1 = "Frage: Bitte wählen Sie die falsche Aussage"
    comprehension_question_2 = "Frage: Die Verhandlungskosten betragen 0,05€ pro Sekunde. Die Verhandlung dauert 20 Sekunden, als der Computer die Verhandlung beendet. Was sind die Verhandlungskosten für den Käufer in Euro?"
  

    section_overview = "Übersicht"
    section_main_task = "Die Verhandlung"

    practice_round_1_title = "Übungsrunde 1 / 3"
    practice_round_1_text = "In dieser Übungsrunde sehen Sie die Umgebung, Sie können Angebote abgeben oder die Verhandlung beenden. Sie spielen nicht gegen andere Spieler, daher wird nichts passieren. Stattdessen beendet der Computer die Verhandlung automatisch nach 30 Sekunden."

    practice_round_2_title = "Übungsrunde 2 / 3"
    practice_round_2_text = "In dieser Übungsrunde verhandeln Sie mit dem Computer. Der Computer macht nach 10 Sekunden ein zufälliges Angebot und verbessert es alle 10 Sekunden. Sie können das Angebot annehmen, es ablehnen, ein Gegenangebot machen oder die Verhandlung beenden. Allerdings wird der Computer keines Ihrer Angebote akzeptieren. Die Verhandlung endet automatisch nach 60 Sekunden."

    practice_round_3_title = "Übungsrunde 3 / 3"
    practice_round_3_text = "In dieser Übungsrunde macht der Computer nach 10 Sekunden ein zufälliges Angebot und verbessert es alle 10 Sekunden. Sie können das Angebot annehmen, es ablehnen, ein Gegenangebot machen oder die Verhandlung beenden. Der Computer wird Ihr zweites Angebot akzeptieren."


    minimum_payoff_text_1 = "Hinweis: Die minimale Auszahlung in diesem Experiment beträgt "
    minimum_payoff_text_2 = "€. Wenn ihr Gewinn in der Runde, die wir für die Auszahlung auswählen, unter "
    minimum_payoff_text_3 = "€ liegt, erhalten Sie als Vergütung "
    minimum_payoff_text_4 = "€."

    comprehension_question_1_choice_1 = "Das Experiment besteht aus 30 Runden."
    comprehension_question_1_choice_2 = "Die Teilnehmer werden zufällig entweder als Käufer oder als Verkäufer zugewiesen."
    comprehension_question_1_choice_3 = "In manchen Runden haben Sie die Rolle des Verkäufers und in anderen Runden die Rolle des Käufers."
    comprehension_question_1_choice_4 = "Zu Beginn jeder Runde werden ein Käufer und ein Verkäufer zufällig gepaart."

    comprehension_question_2_choice_1 = "Die angesammelten Verhandlungskosten werden nicht von der Teilnahmevergütung abgezogen."
    comprehension_question_2_choice_2 = "Die angesammelten Verhandlungskosten werden von der Teilnahmevergütung abgezogen."

    intro_practice_rounds_title = "Beginn der Übungsrunden"
    intro_practice_rounds_1 = "In diesem Experiment sind Sie"
    intro_practice_rounds_2 = "und diese Rolle bleibt während des gesamten Experiments gleich. Bevor das Experiment beginnt, werden Sie drei Übungsrunden durchführen. Der Zweck dieser Übungsrunden ist es, Sie mit der Umgebung vertraut zu machen. Keine Übungsrunde trägt zu Ihrer endgültigen Auszahlung bei."

    intro_real_game_title = "Ende der Übungsrunden"
    intro_real_game = "Jetzt beginnt das eigentliche Experiment. Sie werden mit anderen Experimentteilnehmern für insgesamt 30 Runden verhandeln. Wir werden eine dieser Runden zufällig auswählen, um Ihre endgültige Auszahlung zu berechnen."

    strategy_question_buyer = "Frage: Stellen Sie sich vor, dass Sie ein Käufer sind und um ein Objekt verhandeln, dass Ihnen 20 Euro wert ist. Beschreiben Sie Ihre Strategie für das Verhandlungsszenario. Schreiben Sie mindestens 3 Sätze."
    strategy_question_seller = "Frage: Stellen Sie sich vor, dass Sie ein Verkäufer sind und um ein Objekt verhandeln, dass Ihnen 0 Euro wert ist. Beschreiben Sie Ihre Strategie für das Verhandlungsszenario. Schreiben Sie mindestens 3 Sätze."
    

    #-----------------------------------
    # Results
    #-----------------------------------

    practice_round_results_title_1 = "Ergebnisse dieser Übungsrunde (Übungsrunde"
    practice_round_results_title_2 = "von"
    practice_round_results_title_3 = ")"

    real_game_results_title_1 = "Ergebnisse dieser Runde (Runde"
    real_game_results_title_2 = "von"
    real_game_results_title_3 = ")"

    value_of_object = "Wert des Objekts: "
    price_label = "Preis: "
    no_deal_text = "Keine Einigung"
    gains_from_trade_label = "Gewinn aus Handel: "
    transaction_costs_label = "Transaktionskosten: "
    payoff_from_match_label = "Gewinn aus der Runde: "
    participation_fee_label = "Teilnahmevergütung: "
    total_payoff_label = "Gesamtauszahlung: "


    acceptance_1 = "Sie haben das Preisangebot des anderen Teilnehmers ("
    acceptance_2 = " von "
    acceptance_3 = "€) akzeptiert."

    acceptance_4 = "Der andere Teilnehmer ("
    acceptance_5 = " hat Ihr Angebot ("
    acceptance_6 = "€) akzeptiert."

    payoff_calculation_practice_1 = "Wir würden Ihre Gesamtauszahlung im wirklichen Experiment als "
    payoff_calculation_practice_2 = "€ berechnen. Es wird wie folgt berechnet: "

    payoff_calculation_real_1 = "Wenn diese Runde als Auszahlung relevant gezogen wird, beträgt Ihre Gesamtauszahlung "
    payoff_calculation_real_2 = "€. Es wird wie folgt berechnet: "

    termination_text_computer_1 = "Die Verhandlung wurde vom Computer nach "
    termination_text_computer_2 = " Sekunden beendet."

    termination_text_player_self = "Sie haben die Verhandlung beendet und es wurde keine Einigung erzielt."
    termination_text_player_other = "Die Verhandlung wurde von dem anderen Teilnehmer beendet und es wurde keine Einigung erzielt."

    no_deal_text = "Keine Einigung."


    #-----------------------------------
    # Final Results
    #-----------------------------------

    final_results_title = "Ihre Auszahlung"

    
    final_results_1 = "Runde "
    final_results_2 = " wurde für die Auszahlung ausgewählt. "

    below_minimum_payoff_1 = "Der Gewinn aus dieser Runde wäre: "
    below_minimum_payoff_2 = "€. Allerdings ist dieser Gewinn unter dem Minimum von 7.5€. Deshalb beträgt Ihre endgültige Auszahlung 7.5€."

    final_results_3 = "Das bedeutet, dass das Geld, das Sie für diese Teilnahme im Experiment erhalten, beträgt: "
    final_results_4 = "€. Es wird wie folgt berechnet:"


    final_results_5 = "Die Verhandlung wurde beendet. Deshalb beträgt Ihre endgültige Auszahlung die Teilnahmevergütung abzüglich der Transaktionskosten, also "
    final_results_6 = " - "
    final_results_7 = " = "

    final_results_8 = "Es wurde keine Einigung erzielt in der gegebenen Zeitspanne. Deshalb beträgt Ihre endgültige Auszahlung die Teilnahmevergütung abzüglich der Transaktionskosten, also "
    final_results_9 = " - "
    final_results_10 = " = "


    #-----------------------------------
    #Bargain Page
    #-----------------------------------


    bargain_page_title_practice_1 = "Übungsrunde "
    bargain_page_title_practice_2 = " von "
    bargain_page_title_real_1 = "Runde "
    bargain_page_title_real_2 = " von "

    bargaining_countdown_text = "Die Verhandlung beginnt in 5"

    bargain_page_own_value = "In dieser Runde beträgt der Wert des Objekts für Sie"
    value_of_object_for_seller_0 = "Der Wert des Objekts für den Verkäufer beträgt 0€."
    value_of_object_for_seller_random_60 = "Der Wert des Objekts für den Verkäufer ist eine zufällige Zahl zwischen 0 und 60€."
    value_of_object_for_buyer_30 = "Der Wert des Objekts für den Käufer ist eine zufällige Zahl zwischen 0 und 30€."
    value_of_object_for_buyer_random_60 = "Der Wert des Objekts für den Käufer ist eine zufällige Zahl zwischen 0 und 60€."


    bargain_page_negotiation_costs_heading = "Verhandlungskosten"
    bargain_page_negotiation_costs_current = "Aktuelle Verhandlungskosten pro Sekunde"
    bargain_page_negotiation_costs_total = "Gesamte Verhandlungskosten"

    bargain_time = "Zeit: "
    seconds = " Sekunden"

    bargain_page_current_price_offer = "Ihr aktuelles Preisangebot:"
    
    accept_other_player_offer = "Akzeptieren"

    bargain_page_other_player_accepts_your_current_offer = "Wenn der andere Spieler Ihr aktuelles Angebot akzeptiert:"

    bargain_page_your_payoff = "Ihr Gewinn:"
    bargain_page_payoff_other_player = "Gewinn des anderen Spielers:"

    bargain_page_other_player_current_price_offer = "Aktuelles Preisangebot des anderen Spielers:"

    bargain_page_accept_other_player_offer = "Akzeptiere das Angebot des anderen Spielers"

    bargain_page_if_you_accept_the_offer = "Wenn Sie das Angebot des anderen Spielers akzeptieren:"

    bargain_page_risk_of_termination = "Risiko der Beendigung"

    bargain_page_probability_of_termination = "Die Wahrscheinlichkeit, dass der Computer die Verhandlung in der nächsten Sekunde beendet, beträgt "

    bargain_page_payoffs_heading = "Auszahlungen"

    bargain_page_payoffs_heading_1 = "Wenn ein Angebot akzeptiert wird:"
    bargain_page_payoffs_seller_payoff_ta_costs = "Verkäufer: Akzeptiertes Angebot - Verhandlungskosten"
    bargain_page_payoffs_buyer_payoff_ta_costs = "Käufer: Objektwert Käufer - Akzeptiertes Angebot - Verhandlungskosten"
    bargain_page_payoffs_seller_payoff_0_ta_costs = "Käufer: Objektwert Käufer- Akzeptiertes Angebot"
    bargain_page_payoffs_buyer_payoff_0_ta_costs = "Verkäufer: Akzeptiertes Angebot - Objektwert Verkäufer"

    bargain_page_payoffs_heading_2 = "Wenn der Käufer oder der Verkäufer die Verhandlung beendet:"
    bargain_page_payoffs_both_payoff_ta_costs = "Beide: - Verhandlungskosten"
    bargain_page_payoffs_both_payoff_0_ta_costs = "Beide: 0€"

    bargain_page_terminate_negotiation_button = "Beenden"
    bargain_page_terminate_negotiation = "Verhandlung beenden"
    bargain_page_terminate_negotiation_if_you = "Wenn Sie die Verhandlung beenden:"
    bargain_page_terminate_negotiation_both_payoff = "Beide erhalten eine Auszahlung von: "
    bargain_page_terminate_negotiation_other_payoff = "Gewinn des anderen Spielers:"

    bargain_page_terminate_negotiation_heading = "Beendung der Verhandlung"
    bargain_page_terminate_negotiation_heading_1 = "Wenn Sie die Verhandlung beenden:"
    bargain_page_terminate_negotiation_heading_2 = "Wenn der andere Spieler die Verhandlung beendet:"


    bargain_page_warning_message_buyer = "Ihr Angebot ist höher als der Wert des Objekts für Sie. Sind Sie sicher, dass Sie das Angebot absenden möchten?"
    bargain_page_warning_message_seller = "Ihr Angebot ist niedriger als der Wert des Objekts für Sie. Sind Sie sicher, dass Sie das Angebot absenden möchten?"


#-----------------------------------
# Demographics Preferences
#-----------------------------------

    question_number_one = "Frage 1"
    question_number_two = "Frage 2"
    question_number_three = "Frage 3"
    question_number_four = "Frage 4"
    question_number_five = "Frage 5"
    question_number_six = "Frage 6"

    risk_elicitation_label = "Stellen Sie sich vor, Sie können an einem der folgenden Gewinnspiele teilnehmen. Sie gewinnen entweder mit der angegebenen Wahrscheinlichkeit die angegebene Summe oder nichts. Welches Gewinnspiel würden Sie bevorzugen?"

    risk_elicitation_choice_1 = "80% Wahrscheinlichkeit, 2€ zu gewinnen"
    risk_elicitation_choice_2 = "70% Wahrscheinlichkeit, 3€ zu gewinnen"
    risk_elicitation_choice_3 = "60% Wahrscheinlichkeit, 4€ zu gewinnen"
    risk_elicitation_choice_4 = "50% Wahrscheinlichkeit, 5€ zu gewinnen"
    risk_elicitation_choice_5 = "40% Wahrscheinlichkeit, 6€ zu gewinnen"
    risk_elicitation_choice_6 = "30% Wahrscheinlichkeit, 7€ zu gewinnen"

    ultimatum_proposer_instruction_label = "Ihr Vorschlag:"

    time_preference_label_choice_a = "Jetzt erhalten"
    time_preference_label_choice_b = "In 6 Monaten erhalten"

    gender_male = "männlich"
    gender_female = "weiblich"
    gender_other = "divers"

 

    demographics_preferences_title = "Abschliessende Fragen"
    ultimatum_intro = 'Stellen Sie sich folgende Situation vor: Sie erhalten 50 Euro, und müssen diese zwischen Ihnen und einem anderen zufällig ausgewählten Experimentteilnehmer aufteilen. Nachdem Sie Ihren Vorschlag abgegeben haben, kann der andere Spieler es akzeptieren oder ablehnen. Wenn er es ablehnt, erhalten Sie und der andere Spieler 0 Euro. Wenn er es akzeptiert, erhalten beide das Geld.'

    ultimatum_proposer_instruction = 'Welchen Vorschlag würden Sie abgeben? (0€ - 50€)'
    ultimatum_other_label = "Der andere Spieler erhält:"

    offer_timing_question = "Wie haben Sie entschieden, <strong>zu welchem Zeitpunkt</strong> Sie Ihre Angebote in den Verhandlungen abgeben?"

    age_label = "Wie alt sind Sie?"
    gender_label = "Was ist Ihr Geschlecht?"

    
    time_preference_label = "Stellen Sie sich vor, sie erhalten Geld geschenkt. Sie können wählen, ob sie eine Summe eintweder jetzt, oder eine andere Summe in 6 Monaten erhalten. Für die folgenden 6 Optionen, sagen Sie uns jeweils, welche Sie bevorzugen."







