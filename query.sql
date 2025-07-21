select row_to_json(articles) from  

(select uma.id as article_id, -- analysis_complexity, -- severity, 

(select stt.translation from public.samplemed_translation_translation stt where cast(stt.object_id as varchar) = cast(uma.article_type_id as varchar) and stt.content_type_id = (select id from public.django_content_type ct where ct.model = 'articletype' and app_label = 'underwriting_manual') and field='name' and lang = 'pt-BR' limit 1) as article_type_pt_br, 

(select stt.translation from public.samplemed_translation_translation stt where cast(stt.object_id as varchar) = cast(umac.id as varchar) and stt.content_type_id = (select id from public.django_content_type ct where ct.model = 'articlecategory' and app_label = 'underwriting_manual') and field='name' and lang = 'pt-BR' limit 1) as article_category_pt_br, 

(select stt.translation from public.samplemed_translation_translation stt where cast(stt.object_id as varchar) = cast(uma.id as varchar) and stt.content_type_id = (select id from public.django_content_type ct where ct.model = 'article' and app_label = 'underwriting_manual') and field='name' and lang = 'pt-BR' limit 1) as article_name_pt_br, 

(select stt.translation from public.samplemed_translation_translation stt where cast(stt.object_id as varchar) = cast(uma.id as varchar) and stt.content_type_id = (select id from public.django_content_type ct where ct.model = 'article' and app_label = 'underwriting_manual') and field='description' and lang = 'pt-BR' limit 1) as article_description_pt_br, 

(select stt.translation from public.samplemed_translation_translation stt where cast(stt.object_id as varchar) = cast(uma.risk_id as varchar) and stt.content_type_id = (select id from public.django_content_type ct where ct.model = 'risk' and app_label = 'sample360_underwriting') and field='name' and lang = 'pt-BR' limit 1) as article_risk_pt_br, 

       ( select  
 
           JSONB_AGG(JSONB_BUILD_OBJECT( 
               'code', table_codes.code, 
               'type', table_codes.type 
           )) AS code 
 
          FROM ( 
                   select  id, article_id, code, type 
                    from underwriting_manual_article_codes umac 
                    where umac.article_id = uma.id 
 
            ) table_codes) as icd_codes 
  

, 

        ( select  
 
           JSONB_AGG(JSONB_BUILD_OBJECT( 
               'article_tag_pt_br', table_article_tag.article_tag_pt_br 
           )) AS code 
 
          FROM ( 
                  select  tag_id, 
 
                    (select stt.translation from public.samplemed_translation_translation stt  
                    where cast(stt.object_id as varchar) = cast(umt.tag_id as varchar) 
                    and stt.content_type_id = (select id from public.django_content_type ct where ct.model = 'tag'  
                    and app_label = 'core') and field='description' and lang = 'pt-BR' limit 1) as article_tag_pt_br 
 
                    from underwriting_manual_article_tags umt 
                    inner join core_tag ct on ct.id = umt.tag_id 
                    -- where article_id = 'c8ce6c09-3fee-4681-b16c-7093b1db3a81'  or article_id =  'bd8d9579-dc98-4ece-bc13-465858979c1c' 
                    where umt.article_id = uma.id 
 
            ) table_article_tag) as article_tags 
  

, ( select  

JSONB_AGG(JSONB_BUILD_OBJECT( 'article_property_type_pt_br', table_propertie.article_property_type_pt_br, 'article_property_category_pt_br', article_property_category_pt_br, 'article_property_pt_br', article_property_pt_br, 'tags', tags 

)) AS property_id 

FROM ( 

        select  
 
        (select stt.translation from public.samplemed_translation_translation stt  
        where cast(stt.object_id as varchar) = cast(umap.article_property_type_id as varchar) 
        and stt.content_type_id = (select id from public.django_content_type ct where ct.model = 'articlepropertytype'  
        and app_label = 'underwriting_manual') and field='name' and lang = 'pt-BR' limit 1) as article_property_type_pt_br, 
 
         
        (select stt.translation from public.samplemed_translation_translation stt  
        where cast(stt.object_id as varchar) = cast(umap.article_property_category_id as varchar) 
        and stt.content_type_id = (select id from public.django_content_type ct where ct.model = 'articlepropertycategory'  
        and app_label = 'underwriting_manual') and field='name' and lang = 'pt-BR' limit 1) as article_property_category_pt_br, 
 
        (select stt.translation from public.samplemed_translation_translation stt  
        where cast(stt.object_id as varchar) = cast(umap.id as varchar) 
        and stt.content_type_id = (select id from public.django_content_type ct where ct.model = 'articleproperty'  
        and app_label = 'underwriting_manual') and field='description' and lang = 'pt-BR' limit 1) as article_property_pt_br 
 
          , 
        ( select  
 
           JSONB_AGG(JSONB_BUILD_OBJECT( 
               'article_property_type_pt_br', table_tag.article_property_tag_pt_br 
 
 
           )) AS tag 
 
          FROM ( 
 
                   select 
                    (select stt.translation from public.samplemed_translation_translation stt  
                    where cast(stt.object_id as varchar) = cast(umapt.tag_id as varchar) 
                    and stt.content_type_id = (select id from public.django_content_type ct where ct.model = 'tag'  
                    and app_label = 'core') and field='description' and lang = 'pt-BR' limit 1) as article_property_tag_pt_br 
 
                    from underwriting_manual_article_property_tag umapt 
                    inner join underwriting_manual_article_properties umaptag on umaptag.id = umapt.article_property_id  
                    inner join core_tag ct on ct.id = umapt.tag_id 
 
                    where umapt.article_property_id = umap.id 
 
            ) table_tag) as tags 
 
   
   
        from underwriting_manual_article_properties umap 
        inner join underwriting_manual_articles uma2 on uma2.id = umap.article_id 
         
          where uma2.id = uma.id  
   
) table_propertie) as properties 
  

, 

        ( select  
 
           JSONB_AGG(JSONB_BUILD_OBJECT( 
               'risk_axiom_pt_br', table_axioms.risk_axiom_pt_br 
                  )) AS axiom_t 
 
          FROM ( 
                   
              select   
                -- ura.id as risk_axiom_id,  
                -- risk_axiom_type,  
                -- risk_axiom_answer_type_id, 
                -- risk_axiom_trait_type_id, 
                -- financial_formula_id, 
 
                (select stt.translation from public.samplemed_translation_translation stt  
                 where cast(stt.object_id as varchar) = cast(ura.id as varchar) 
                and stt.content_type_id = (select id from public.django_content_type ct where ct.model = 'riskaxiom'  
                and app_label = 'sample360_underwriting') and field='name' and lang = 'pt-BR' limit 1) as risk_axiom_pt_br 
               
 
                 from public.underwriting_manual_articles uma_a 
                inner join underwriting_risk_axioms ura on ura.risk_id = uma_a.risk_id 
                inner join underwriting_risk_axiom_answer_options urao on urao.risk_axiom_id = ura.id 
                 
                where uma_a.id = uma.id 
                  group by risk_axiom_pt_br 
 
            ) table_axioms) as risk_analisys_question_requirements 
  

from public.underwriting_manual_articles uma left join public.underwriting_manual_article_categories umac on uma.article_category_id = umac.id 

-- where uma.id = 'c8ce6c09-3fee-4681-b16c-7093b1db3a81' or uma.id = 'bd8d9579-dc98-4ece-bc13-465858979c1c' 

) as articles 
