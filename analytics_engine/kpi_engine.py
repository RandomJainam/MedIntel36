"""
=========================================================
MedIntel360
KPI Engine
=========================================================

Reusable KPI calculations for the entire project.

Author : Jainam Gada
"""

import numpy as np
import pandas as pd


class KPIEngine:

    """
    Enterprise KPI Engine

    Every KPI is implemented only once
    and reused everywhere.
    """

    # =====================================================
    # Patient KPIs
    # =====================================================

    @staticmethod
    def department_average_los(df):

        df["department_average_los"] = (

            df.groupby("department_name")["los"]

            .transform("mean")

            .round(2)

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def department_average_revenue(df):

        df["department_average_revenue"] = (

            df.groupby("department_name")["total_amount"]

            .transform("mean")

            .round(2)

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def patient_lifetime_revenue(df):

        df["patient_lifetime_revenue"] = (

            df.groupby("patient_id")["total_amount"]

            .transform("sum")

            .round(2)

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def patient_visit_count(df):

        df["patient_visit_count"] = (

            df.groupby("patient_id")["admission_id"]

            .transform("count")

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def frequent_patient_flag(df):

        df["frequent_patient_flag"] = np.where(

            df["patient_visit_count"] > 2,

            1,

            0

        )

        return df

    # =====================================================
    # Patient Performance KPIs
    # =====================================================
   

    @staticmethod
    def revenue_performance(df):

        df["revenue_performance"] = np.where(

            df["total_amount"]

            >=

            df["department_average_revenue"],

            "High",

            "Low"

        )

        return df

    # -----------------------------------------------------

    


    @staticmethod
    def los_performance(df):

        df["los_performance"] = np.where(

            df["los"]

            <=

            df["department_average_los"],

            "Good",

            "Needs Attention"

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def department_admission_count(df):

        df["department_admission_count"] = (

            df.groupby("department_name")["admission_id"]

            .transform("count")

        )

        return df

    # =====================================================
    # Master Pipeline
    # =====================================================

    @staticmethod
    def build_patient_kpis(df):

        # Department KPIs
        df = KPIEngine.department_average_los(df)
        df = KPIEngine.department_average_revenue(df)
        df = KPIEngine.department_admission_count(df)

        # Patient KPIs
        df = KPIEngine.patient_lifetime_revenue(df)
        df = KPIEngine.patient_visit_count(df)
        df = KPIEngine.frequent_patient_flag(df)

        # Performance KPIs
        df = KPIEngine.los_performance(df)
        df = KPIEngine.revenue_performance(df)

        return df
    
    # =====================================================
    # Finance KPIs
    # =====================================================

    @staticmethod
    def average_revenue(df):

        df["average_revenue"] = (

            df.groupby("department_name")["amount"]

            .transform("mean")

            .round(2)

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def department_total_revenue(df):

        df["department_total_revenue"] = (

            df.groupby("department_name")["amount"]

            .transform("sum")

            .round(2)

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def department_revenue_rank(df):

        df["department_revenue_rank"] = (

            df["department_total_revenue"]

            .rank(

                ascending=False,

                method="dense"

            )

        )

        return df
    
    # -----------------------------------------------------

    @staticmethod
    def payment_completion_ratio(df):

        df["payment_completion_ratio"] = np.where(

            df["payment_status"] == "Paid",

            1,

            0

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def insurance_coverage_percentage(df):

        revenue = df["total_amount"].replace(0, 1)

        df["insurance_coverage_percentage"] = (

            df["insurance_covered_amount"]

            /

            revenue

            * 100

        ).round(2)

        return df

    # -----------------------------------------------------

    @staticmethod
    def patient_payment_percentage(df):

        revenue = df["total_amount"].replace(0, 1)

        df["patient_payment_percentage"] = (

            df["patient_payable_amount"]

            /

            revenue

            * 100

        ).round(2)

        return df

    # -----------------------------------------------------

    @staticmethod
    def department_revenue_share(df):

        hospital_total = df["amount"].sum()

        department_total = (

            df.groupby("department_name")["amount"]

            .transform("sum")

        )

        df["department_revenue_share"] = (

            department_total

            /

            hospital_total

            * 100

        ).round(2)

        return df

    # -----------------------------------------------------

    @staticmethod
    def charge_type_count(df):

        if "charge_type" in df.columns:

            df["charge_type_count"] = (

                df.groupby("charge_type")["billing_detail_id"]

                .transform("count")

            )

        return df

    # -----------------------------------------------------

    @staticmethod
    def high_coverage_flag(df):

        if "maximum_coverage_percentage" in df.columns:

            df["high_coverage_flag"] = np.where(

                df["maximum_coverage_percentage"] >= 80,

                1,

                0

            )


        else:

            df["high_coverage_flag"] = 0

        return df

    @staticmethod
    def top_department_flag(df):

        df["top_department_flag"] = np.where(

            df["department_revenue_rank"] <= 3,

            1,

            0

        )

        return df
    # -----------------------------------------------------

    @staticmethod
    def build_finance_kpis(df):

        df = KPIEngine.average_revenue(df)

        df = KPIEngine.department_total_revenue(df)

        df = KPIEngine.department_revenue_rank(df)

        df = KPIEngine.payment_completion_ratio(df)

        df = KPIEngine.insurance_coverage_percentage(df)

        df = KPIEngine.patient_payment_percentage(df)

        df = KPIEngine.department_revenue_share(df)

        df = KPIEngine.charge_type_count(df)

        df = KPIEngine.high_coverage_flag(df)
        
        df = KPIEngine.top_department_flag(df)

        return df


    # =====================================================
    # Operations KPIs
    # =====================================================

    @staticmethod
    def ward_admission_count(df):

        df["ward_admission_count"] = (

            df
            .groupby("ward_name")["admission_id"]
            .transform("count")

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def ward_occupancy_rate(df):

        beds = df["total_beds"].replace(0, 1)

        df["ward_occupancy_rate"] = (

            df["ward_admission_count"]

            /

            beds

            * 100

        ).round(2)

        return df

    # -----------------------------------------------------

    @staticmethod
    def staff_to_bed_ratio(df):

        beds = df["total_beds"].replace(0, 1)

        df["staff_to_bed_ratio"] = (

            df["staff_count"]

            /

            beds

        ).round(2)

        return df

    # -----------------------------------------------------

    @staticmethod
    def doctor_to_staff_ratio(df):

        staff = df["staff_count"].replace(0, 1)

        df["doctor_to_staff_ratio"] = (

            df["doctor_count"]

            /

            staff

        ).round(2)

        return df

    # -----------------------------------------------------

    @staticmethod
    def nurse_to_staff_ratio(df):

        staff = df["staff_count"].replace(0, 1)

        df["nurse_to_staff_ratio"] = (

            df["nurse_count"]

            /

            staff

        ).round(2)

        return df

    # -----------------------------------------------------

    @staticmethod
    def technician_to_staff_ratio(df):

        staff = df["staff_count"].replace(0, 1)

        df["technician_to_staff_ratio"] = (

            df["technician_count"]

            /

            staff

        ).round(2)

        return df

    # -----------------------------------------------------

    @staticmethod
    def night_shift_percentage(df):

        shifts = df["shift_count"].replace(0, 1)

        df["night_shift_percentage"] = (

            df["night_shift_count"]

            /

            shifts

            * 100

        ).round(2)

        return df

    # -----------------------------------------------------

    @staticmethod
    def occupied_bed_flag(df):

        df["occupied_bed_flag"] = np.where(

            df["bed_status"] == "Occupied",

            1,

            0

        )

        return df

    # -----------------------------------------------------

    @staticmethod
    def high_workload_ward_flag(df):

        threshold = df["ward_admission_count"].median()

        df["high_workload_ward_flag"] = np.where(

            df["ward_admission_count"] >= threshold,

            1,

            0

        )

        return df

    # =====================================================
    # Master Pipeline
    # =====================================================

    @staticmethod
    def build_operations_kpis(df):

        df = KPIEngine.ward_admission_count(df)

        df = KPIEngine.ward_occupancy_rate(df)

        df = KPIEngine.staff_to_bed_ratio(df)

        df = KPIEngine.doctor_to_staff_ratio(df)

        df = KPIEngine.nurse_to_staff_ratio(df)

        df = KPIEngine.technician_to_staff_ratio(df)

        df = KPIEngine.night_shift_percentage(df)

        df = KPIEngine.occupied_bed_flag(df)

        df = KPIEngine.high_workload_ward_flag(df)

        return df