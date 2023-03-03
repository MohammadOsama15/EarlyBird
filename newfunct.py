@main.route('/search')
@login_required
def search():
    form_data = request.args
    query_text = form_data.get("searchTerm")
    time = datetime.now() - timedelta(hours=24)
    try:
        # Check if the query is already in the database
        query = Query.query.filter_by(query_text=query_text).first()
        if query:
            if query.time > time:
                # If the query is in the database and was made within the last 24 hours, retrieve the results from the database
                results = [result.title for result in query.results]
                predictions = [result.sentiment for result in query.results]
            else:
                # If the query is more than 24 hours old, delete it and make a new API call to retrieve the search results
                db.session.delete(query)
                db.session.commit()
                results = search_posts(query_text, cap=None)
                if results:
                    # Add the new query and results to the database
                    query = Query(query_text=query_text, time=datetime.now())
                    db.session.add(query)
                    db.session.commit()
                    # Perform inference on the search results
                    tokenized_sequence = tokenize_sequence([result.get('selftext') if isinstance(result, dict) else result for result in results])
                    predictions = model.predict(tokenized_sequence)

                    for result, prediction in zip(results, predictions):
                        if isinstance(result, str):
                            new_result = Result(title=result, sentiment=prediction, query=query)
                        else:
                            new_result = Result(title=result.get('title'), sentiment=prediction, query=query)
                        db.session.add(new_result)

                    db.session.commit()
                else:
                    predictions = []
        else:
            # Perform a new search
            results = search_posts(query_text, cap=None)
            if results:
                # Add the query and results to the database
                query = Query(query_text=query_text, time=datetime.now())
                db.session.add(query)
                db.session.commit()
                # Perform inference on the search results
                tokenized_sequence = tokenize_sequence([result.get('selftext') if isinstance(result, dict) else result for result in results])
                predictions = model.predict(tokenized_sequence)

                for result, prediction in zip(results, predictions):
                    if isinstance(result, str):
                        new_result = Result(title=result, sentiment=prediction, query=query)
                    else:
                        new_result = Result(title=result.get('title'), sentiment=prediction, query=query)
                    db.session.add(new_result)

                db.session.commit()
            else:
                results = []
                predictions = []

        if results:
            # Zip the predictions and headlines together for display
            display = zip(predictions, [result.title if isinstance(result, dict) else result for result in results])
            return render_template("search.html", display=display)
        else:
            return render_template("search.html")
    except Exception as e:
        return render_template("error.html", error=str(e))
