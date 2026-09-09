
# this file comapres resume against Job description

from preprocess import normalise_text
from sentence_transformers import SentenceTransformer, util
#from  test_preprocess import resume_text 


# this function returns score percentage m matched keywords and missed keywords 

def compute_ats_score(jd_keywords: list[str],resume_text: str) ->dict:
    normalised_resume = normalise_text(resume_text)
    matched=[]
    missing=[]
    for keywords in jd_keywords:
        if keywords in normalised_resume:
            matched.append(keywords)
        else:
            missing.append(keywords)
            
    total = len(jd_keywords)
    total_matched=len(matched)
    score= round((len(matched)/total)*100,1) if total>0 else 0.0
    return{
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "total_keywords":total,
        "total_matched_keywords":total_matched
    }

semantic_model=SentenceTransformer('BAAI/bge-small-en-v1.5')

## this function wasn't working well in the execution time because mising words were checked against bullt lines
# means one words against a sentence or line which cause aavaerage of sentence vectors and diluting the 
# the context and displaying that no words matches 
# solution one i came across lowering the threshold from 0.75 to 0.55 to 0.3 but its a bad idea becuse it let in 
# false positives like matching kubernets to python programming becuase they both are tech words.
# solution two :using cross encoder instead of bi-encoder moder , bi encoder creates vector for both elements independently while
# cross encoder takes both elements together and then creates a vector for them which is more accurate but slower
# like passes the keyword and the resume bullet into the transformer together, allowing the attention mechanism to 
# directly calculate exactly how much the bullet cares about that specific keyword. It is highly accurate for short-to-long text matching.

# third solution: i can use a specific model trained for professional tech and coroporate vocab like BAAI/bge-small-en-v1.5 or 
# a dedicated tech/resume embedding model.


def semantic_keywords(missing_keywords: list[str],resume_bullets: list[str], threshold: float=0.7) ->dict:
    new_matched=[]
    still_missing=[]
    
    for keyword in missing_keywords:
        keywords_embedding=semantic_model.encode(keyword)
        bullet_embedding=semantic_model.encode(resume_bullets)
        cosine_sim=util.cos_sim(keywords_embedding,bullet_embedding)
        best_score= float(cosine_sim.max())
        
        if best_score>=threshold:
            new_matched.append(keyword)
        else:
            still_missing.append(keyword)
    return {"new_matched": new_matched, "still_missing":still_missing}

if __name__=="__main__":
    from keywords import jd_keywords
    from test_preprocess import resume_text
    ats_result= compute_ats_score(jd_keywords,resume_text)
    print("----ATS SCORE-----")
    print("Score:", ats_result["score"])
    print("Matched Keywords:", ats_result["matched_keywords"])
    print("Missing Keywords:", ats_result["missing_keywords"])
    print("Total Keywords:", ats_result["total_keywords"])
    print("Total Matched Keywords:", ats_result["total_matched_keywords"])