-- sql_queries.sql
-- SQL-based data extraction and transformation pipelines
-- for operational risk heatmap reporting
-- Aligned to best practices in data storage, retrieval, and manipulation

-- ============================================================
-- 1. Control effectiveness summary by business unit
-- ============================================================
SELECT
    business_unit,
    COUNT(control_id)                          AS total_controls,
    ROUND(AVG(assessment_score), 2)            AS avg_assessment_score,
    SUM(CASE WHEN assessment_score < 60
             THEN 1 ELSE 0 END)               AS weak_controls,
    SUM(CASE WHEN frequency_of_failure > 3
             THEN 1 ELSE 0 END)               AS high_failure_controls,
    SUM(CASE WHEN regulatory_impact = 'High'
             THEN 1 ELSE 0 END)               AS high_reg_impact_controls
FROM control_assessments
GROUP BY business_unit
ORDER BY avg_assessment_score ASC;


-- ============================================================
-- 2. Top 10 weakest controls for escalation to senior management
-- ============================================================
SELECT
    control_id,
    business_unit,
    control_name,
    risk_dimension,
    assessment_score,
    frequency_of_failure,
    regulatory_impact,
    operational_impact,
    last_assessed
FROM control_assessments
WHERE assessment_score < 65
   OR frequency_of_failure >= 3
ORDER BY assessment_score ASC,
         frequency_of_failure DESC
LIMIT 10;


-- ============================================================
-- 3. Risk heatmap data — cross-tab of business unit vs risk dimension
-- ============================================================
SELECT
    business_unit,
    risk_dimension,
    COUNT(control_id)               AS control_count,
    ROUND(AVG(assessment_score), 2) AS avg_score,
    MAX(frequency_of_failure)       AS max_failures
FROM control_assessments
GROUP BY business_unit, risk_dimension
ORDER BY avg_score ASC;


-- ============================================================
-- 4. Automated vs manual control effectiveness comparison
-- ============================================================
SELECT
    is_automated,
    COUNT(control_id)                AS total_controls,
    ROUND(AVG(assessment_score), 2)  AS avg_score,
    ROUND(AVG(frequency_of_failure), 2) AS avg_failures,
    SUM(CASE WHEN assessment_score >= 80
             THEN 1 ELSE 0 END)     AS strong_controls
FROM control_assessments
GROUP BY is_automated;


-- ============================================================
-- 5. Controls overdue for reassessment (>60 days since last assessed)
-- ============================================================
SELECT
    control_id,
    business_unit,
    control_name,
    last_assessed,
    DATEDIFF(CURRENT_DATE, last_assessed) AS days_since_assessment,
    assessment_score,
    regulatory_impact
FROM control_assessments
WHERE DATEDIFF(CURRENT_DATE, last_assessed) > 60
ORDER BY days_since_assessment DESC;
