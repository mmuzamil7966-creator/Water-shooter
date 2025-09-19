def generate_level(level_number):
    # Define parameters based on level number
    params = get_difficulty_parameters(level_number) # e.g., {total_tubes: 7, color_count: 5, empty_tubes: 2, has_locked_tube: True}
    
    # 1. Start from a solved state
    solved_tubes = []
    for color in range(1, params.color_count + 1):
        # Add 4 units of each color to a tube
        solved_tubes.append([color] * 4)
    # Add empty tubes
    for i in range(params.empty_tubes):
        solved_tubes.append([])
        
    # 2. Scramble by performing valid reverse moves
    current_state = solved_tubes
    number_of_scramble_moves = calculate_scramble_moves(level_number) # e.g., level 10 -> 8 moves, level 50 -> 20 moves
    
    for move in range(number_of_scramble_moves):
        # Choose a random non-empty tube to be the *destination* of the reverse move (this will be the source in the actual game)
        possible_destinations = [i for i, tube in enumerate(current_state) if len(tube) > 0]
        dest_index = random.choice(possible_destinations)
        
        # The top color of the chosen tube
        color_to_move = current_state[dest_index][-1]
        
        # Find a source tube (empty in the reverse move) that can receive this color
        # Rules: Tube must not be full, and if it's not empty, the top color must match.
        possible_sources = []
        for i, tube in enumerate(current_state):
            if i == dest_index:
                continue
            if len(tube) < 4: # Tube is not full
                if len(tube) == 0 or tube[-1] == color_to_move:
                    possible_sources.append(i)
                    
        if possible_sources:
            source_index = random.choice(possible_sources)
            # Perform the reverse move: pour from 'destination' back to 'source'
            # In the reverse move, we are "pouring" the top color from the destination back onto the source.
            unit = current_state[dest_index].pop() # Remove from "destination"
            current_state[source_index].append(unit) # Add to "source"
            
    # 3. Apply special mechanics (e.g., lock random tubes, set move limit)
    if params.has_locked_tube:
        lock_random_tube(current_state, params)
        
    # 4. Final check: Run a quick solvability validator on current_state
    if not is_solvable(current_state):
        # If by chance it's unsolvable, retry the generation
        return generate_level(level_number)
        
    return current_state, params.move_limit
