from typing import Literal, Dict

fine_linktype_map = {
    'Backports': 'Backport', 

    'Blocked': 'Block',
    'Blocker': 'Block',
    'Blocks': 'Block',

    'Bonfire Testing': 'Bonfire Testing', 
    'Bonfire testing': 'Bonfire Testing', 
    'Git Code Review': 'Bonfire Testing', 
    'Testing': 'Bonfire Testing',

    'Causality': 'Cause', 
    'Cause': 'Cause',
    'Caused': 'Cause', 
    'Problem/Incident': 'Cause',

    'Child-Issue': 'Parent-Child', 
    'Parent Feature': 'Parent-Child',
    'Parent/Child': 'Parent-Child',
    'multi-level hierarchy [GANTT]': 'Parent-Child',
    'Parent-Relation': 'Parent-Child',

    'Cloners': 'Clone', 
    'Cloners (old)': 'Clone', 

    'Collection': 'Incorporate', 
    'Container': 'Incorporate',
    'Contains(WBSGantt)': 'Incorporate', 
    'Incorporate': 'Incorporate', 
    'Incorporates': 'Incorporate', 
    'Part': 'Incorporate',
    'PartOf': 'Incorporate',
    'Superset': 'Incorporate', 

    'Completes': 'Fix', 
    'Fixes': 'Fix',
    'Resolve': 'Fix',

    'Depend': 'Depend', 
    'Dependency': 'Depend', 
    'Dependent': 'Depend', 
    'Depends': 'Depend', 
    'Gantt Dependency': 'Depend',
    'dependent': 'Depend',

    'Derived': 'Derive',

    'Detail': 'Detail', 

    'Documentation': 'Documented',
    'Documented': 'Documented',
    
    'Duplicate': 'Duplicate',

    'Epic': 'Epic', 
    'Epic-Relation': 'Epic',
    
    'Finish-to-Finish link (WBSGantt)': 'finish-finish', 
    'Gantt End to End': 'finish-finish', 
    'Gantt: finish-finish': 'finish-finish',
    'finish-finish [GANTT]': 'finish-finish', 
    
    'Gantt End to Start': 'finish-start', 
    'Gantt: finish-start': 'finish-start',
    'finish-start [GANTT]': 'finish-start',

    'Gantt Start to Start': 'start-start', 
    
    'Gantt: start-finish': 'start-finish', 
    
    'Follows': 'Follow', 
    'Sequence': 'Follow', 
    
    'Implement': 'Implement', 
    'Implements': 'Implements', 
    
    'Issue split': 'Split',
    'Split': 'Split',
    'Work Breakdown': 'Split',
    
    'Preceded By': 'Precede', 
    
    'Reference': 'Relate',
    'Relate': 'Relate',
    'Related': 'Relate', 
    'Relates': 'Relate',
    'Relationship': 'Relate',
    
    'Regression': 'Breaks', 
    
    'Replacement': 'Replace',
    
    'Required': 'Require', 
    
    'Supercedes': 'Supercede',
    'Supersede': 'Supercede',
    'Supersession': 'Supercede', 
    
    'Subtask': 'Subtask',
    
    'Test': 'Test', 
    'Tested': 'Test',
    
    'Trigger': 'Trigger', 
    
    'Non-Link': 'Non-Link',
          
    '1 - Relate': 'Relate',
    '5 - Depend':   'Depend',          
    '3 - Duplicate': 'Duplicate',          
    '4 - Incorporate': 'Incorporate',        
    '2 - Cloned': 'Clone',    
    '6 - Blocks': 'Block',     
    '7 - Git Code Review': 'Bonfire Testing',
    'Verify': 'Verify'
}

fine_linktype_to_category_map = {
    'Block': 'Causal',
    'Bonfire Testing': 'Workflow',
    'Breaks': 'Causal',
    'Cause': 'Causal',
    'Clone': 'General',
    'Depend': 'Causal',
    'Detail': 'Workflow',
    'Documented': 'Workflow',
    'Duplicate': 'General',
    'Epic': 'Epic',
    'Fix': 'Workflow',
    'Follow': 'Causal',
    'Incorporate': 'Split',
    'Parent-Child': 'Split',
    'Relate': 'General',
    'Replace': 'General',
    'Require': 'Causal',
    'Split': 'Split',
    'Subtask': 'Split',
    'Supercede': 'Causal',
    'Trigger': 'Workflow',
    'finish-start': 'Causal',
    'Non-Link': 'Non-Link',
    'Verify': 'Workflow'
}

category_map = {
    input_linktype: fine_linktype_to_category_map[fine_linktype]
    for input_linktype, fine_linktype in fine_linktype_map.items()
    if fine_linktype in fine_linktype_to_category_map
}

non_link_name = 'Non-Link'


Target = Literal['linktype', 'category']

linktype_map: Dict[Target, Dict[str, str]] = {
    'linktype': fine_linktype_map,
    'category': category_map,
}
