def general():
    return [
    {
        'static': {
            'type':'all',
        },
        'dynamic':{
            'subject':'Subject_ID',
            'excluded': 'excluded',
            'trials': 'trials_total',
            'd-prime': 'd-prime',
            'beta':'beta',
            'c':'c',
            'Ad':'Ad'
        }
    },
    {
        'static': {
            'type': 'diatonic',
        },
        'dynamic': {
            'subject': 'Subject_ID',
            'excluded': 'excluded',
            'trials': 'trials_diatonic',
            'd-prime': 'diatonic_d-prime',
            'beta': 'diatonic_beta',
            'c': 'diatonic_c',
            'Ad': 'diatonic_Ad',
            # 'confidence':'diatonic_confidence',
            # 'confidence_correct': 'diatonic_correct_confidence',
            # 'conf_to_mean': 'diatonic_conf_to_mean',
            # 'conf_correct_to_mean': 'diatonic_correct_conf_to_mean',

        }
    },
    {
        'static': {
            'type': 'chromatic',
        },
        'dynamic': {
            'subject': 'Subject_ID',
            'excluded': 'excluded',
            'trials': 'trials_chromatic',
            'd-prime': 'chromatic_d-prime',
            'beta': 'chromatic_beta',
            'c': 'chromatic_c',
            'Ad': 'chromatic_Ad',
            # 'confidence': 'chromatic_confidence',
            # 'confidence_correct': 'chromatic_correct_confidence',
            # 'conf_to_mean': 'chromatic_conf_to_mean',
            # 'conf_correct_to_mean': 'chromatic_correct_conf_to_mean',

        }
    }

]

def confidence():
    return [
    {
        'static': {
            'type':'all',
        },
        'dynamic':{
            'subject':'Subject_ID',
            'excluded': 'excluded',
            'conf_d:c': 'conf_d:c',
            'conf_correct_d:c':'conf_correct_d:c'
        }
    },


]



